from .utils import *
from ..routers.user import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["id"] == test_user.id
    assert body["username"] == "raizel"
    assert body["email"] == "raizel@test.com"
    assert body["first_name"] == "Raizel"
    assert body["last_name"] == "Lee"
    assert body["role"] == "admin"
    assert body["phone_number"] == "0912345678"
    assert body["is_active"] is True

    assert "hashed_password" not in body
    assert "password" not in body

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