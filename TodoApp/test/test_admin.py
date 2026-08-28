from http.client import responses

from starlette import status

from .utils import *
from ..routers.admin import get_db, get_current_user
from ..models import Todos
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == 200
    assert response.json() == [{'priority': 2, 'id': 1, 'owner_id': 1, 'title': 'Test', 'description': 'Test', 'complete': False}]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/99999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}

def override_get_current_normal_user():
    return {
        "username": "normal_user",
        "id": 2,
        "role": "user",
    }

def test_normal_user_cannot_access_admin_endpoint():
    # 暫時把登入身分改成一般使用者
    app.dependency_overrides[get_current_user] = (
        override_get_current_normal_user
    )

    try:
        response = client.get("/admin/todo")
    finally:
        # 測試結束後恢復原本的 admin override，
        # 避免影響其他 test_admin 測試
        app.dependency_overrides[get_current_user] = (
            override_get_current_user
        )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Admin access required",
    }