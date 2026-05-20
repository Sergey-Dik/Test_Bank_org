import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.utils.api_assertions import assert_ok_json, assert_unauthorized


@pytest.mark.api
@pytest.mark.regression
class TestAdminListUsers:
    def test_admin_list_users_contains_admin(self, api_manager: ApiManager):
        response = api_manager.admin_steps.list_users()
        users = assert_ok_json(response)
        assert isinstance(users, list), "Users list should be returned"
        assert any(user.get("username") == "admin" for user in users), (
            "Admin user should be in list"
        )

    def test_admin_list_users_unauthorized(self, api_manager: ApiManager):
        response = api_manager.admin_steps.list_users_unauthorized()
        assert_unauthorized(response)
