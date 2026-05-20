import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.utils.helpers.api_assertions import assert_ok_model, assert_unauthorized


@pytest.mark.api
class TestUserLogin:
    @pytest.mark.smoke
    def test_login_admin(self, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)
        result = assert_ok_model(response, LoginUserResponse)
        assert login_user_request.username == result.user.username, "Username should match"
        assert result.user.role == "ROLE_ADMIN", "Admin role expected"

    @pytest.mark.smoke
    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.login_user(create_user_request)
        result = assert_ok_model(response, LoginUserResponse)
        assert create_user_request.username == result.user.username, "Username should match"
        assert result.user.role == "ROLE_USER", "User role expected"

    @pytest.mark.regression
    def test_login_user_invalid(self, api_manager: ApiManager, db_session):
        login_user_request = LoginUserRequest(username="Ma", password="Pas!sw0rd")
        response = api_manager.user_steps.login_invalid(login_user_request)
        assert_unauthorized(response)
        DbAssertions.assert_user_not_exists(db_session, login_user_request.username)
