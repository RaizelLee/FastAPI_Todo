from .utils import *
from ..routers.user import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0] ['username']== 'raizel'
    assert response.json()[0] ['email']== 'raizel@test.com'
    assert response.json() [0]['first_name']== 'Raizel'
    assert response.json()[0] ['last_name']== 'Lee'
    assert response.json()[0]['role'] == 'admin'
    assert response.json()[0]['phone_number']== '0912345678'

def test_change_password_success(test_user):
    response = client.put("/user", json={"old_password": "testpassword", "new_password": "newpassword", "new_password_retype":"newpassword"})
    assert response.status_code == status.HTTP_200_OK

def test_change_password_invalid_current_password(test_user):
    response = client.put("/user", json={"old_password": "wrongtestpassword", "new_password": "newpassword",
                                         "new_password_retype": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_change_phone_number_success(test_user):
    response = client.put("/user/phone_number", json={"phone_number": "09111111111"})
    assert response.status_code == status.HTTP_200_OK