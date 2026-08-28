from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, User
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    )

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'raizel', 'id':1, 'role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title='Test',
        description='Test',
        priority=2,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()


@pytest.fixture
def test_user():
    user = User(
        username='raizel',
        email='raizel@test.com',
        first_name='Raizel',
        last_name='Lee',
        hashed_password=bcrypt_context.hash("testpassword"),
        role='admin',
        phone_number = '0912345678'
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()