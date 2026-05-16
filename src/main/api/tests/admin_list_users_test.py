import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.specs.contract_specs import ContractSpecs


@pytest.mark.api
@pytest.mark.regression
class TestAdminListUsers:
    def test_admin_list_users_contains_admin(self, api_manager: ApiManager):
        users = api_manager.admin_steps.list_users()
        assert isinstance(users, list)
        assert any(user.get("username") == "admin" for user in users)

    def test_admin_list_users_unauthorized(self, api_manager: ApiManager):
        response = api_manager.admin_steps.list_users_unauthorized()
        ContractSpecs.assert_error_payload(response.json())
