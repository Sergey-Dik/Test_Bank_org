import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def user_first_account(
    api_manager: ApiManager, create_user_request: CreateUserRequest
) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(create_user_request)


@pytest.fixture
def user_two_accounts(
    api_manager: ApiManager, create_user_request: CreateUserRequest
) -> tuple[CreateAccountResponse, CreateAccountResponse]:
    first = api_manager.user_steps.create_account(create_user_request)
    second = api_manager.user_steps.create_account(create_user_request)
    return first, second
