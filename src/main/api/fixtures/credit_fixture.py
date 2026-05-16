import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.generators.test_data_strategy import with_unique_username
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def credit_secret_user(api_manager: ApiManager):
    user_request = with_unique_username(
        RandomModelGenerator.generate(
            CreateUserRequest,
        )
    )
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    account = api_manager.user_steps.create_account(user_request)
    return user_request, account
