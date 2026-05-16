import pytest

from src.main.api.classes.api_manager import ApiManager


@pytest.mark.api
@pytest.mark.regression
class TestAdminListUsers:
    def test_admin_list_users_contains_admin(self, api_manager: ApiManager):
        users = api_manager.admin_steps.list_users()
        assert isinstance(users, list)
        assert any(user.get("username") == "admin" for user in users)
