from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.sql.annotation import Annotated
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status

from ..models import User
from ..database import engine, SessionLocal
from ..routers import auth
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

from pydantic import BaseModel, ConfigDict, EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    phone_number: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_model = db.query(User).filter(User.id==user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user_model

class PasswordRequest(BaseModel):
    old_password: str = Field(min_length=3)
    new_password: str = Field(min_length=3)
    new_password_retype: str = Field(min_length=3)

class PhoneNumberRequest(BaseModel):
    phone_number: str = Field(min_length=6)

@router.put("/", status_code=status.HTTP_200_OK)
async def update_user(user: user_dependency, db: db_dependency, password_request: PasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    user_model = db.query(User).filter(User.id==user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    if not bcrypt_context.verify(password_request.old_password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if password_request.new_password != password_request.new_password_retype:
        raise HTTPException(status_code=401, detail='Verify password wrong')
    user_model.hashed_password = bcrypt_context.hash(password_request.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phone_number", status_code=status.HTTP_200_OK)
async def update_user_phone_number (user: user_dependency, db: db_dependency, phone_number: PhoneNumberRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    user_model = db.query(User).filter(User.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    user_model.phone_number = phone_number.phone_number
    db.add(user_model)
    db.commit()
