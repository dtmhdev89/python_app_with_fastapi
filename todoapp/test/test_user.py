from todoapp.test.utils import app, client, override_get_db, \
    override_get_current_user, TestingSessionLocal
from todoapp.routers.user import get_db, get_current_user, \
    UpdateUserPasswordForm
from todoapp.models import Users
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")

    assert response.status_code == status.HTTP_200_OK
    json_response = response.json()
    assert json_response["username"] == "testuser"
    assert json_response["email"] == "test@local.email"


def test_change_password_success(test_user):
    request_form = UpdateUserPasswordForm(
        old_password="abc123",
        password="testpassword",
        password_confirmation="testpassword"
    )

    response = client.put("/user/password", json=request_form.model_dump())

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    request_form = UpdateUserPasswordForm(
        old_password="wrong_old_password",
        password="testpassword",
        password_confirmation="testpassword"
    )

    response = client.put("/user/password", json=request_form.model_dump())

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Error on password change"}
