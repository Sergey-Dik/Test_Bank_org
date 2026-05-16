import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.contract_specs import ContractSpecs


@pytest.mark.api
class TestUserLogin:
    @pytest.mark.smoke
    def test_login_admin(self, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)
        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    @pytest.mark.smoke
    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.login_user(create_user_request)
        assert create_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"

    @pytest.mark.regression
    def test_login_user_invalid(self, api_manager: ApiManager, db_session):
        login_user_request = LoginUserRequest(username="Ma", password="Pas!sw0rd")
        response = api_manager.user_steps.login_invalid(login_user_request)
        ContractSpecs.assert_error_payload(response.json())
        DbAssertions.assert_user_not_exists(db_session, login_user_request.username)
