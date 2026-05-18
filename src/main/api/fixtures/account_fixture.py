import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.configs.business_limits import get_limits
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_two_accounts_context import UserTwoAccountsContext


@pytest.fixture
def user_first_account(
    api_manager: ApiManager, create_user_request: CreateUserRequest
) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(create_user_request)


@pytest.fixture
def user_two_accounts(
    api_manager: ApiManager, create_user_request: CreateUserRequest
) -> UserTwoAccountsContext:
    first = api_manager.user_steps.create_account(create_user_request)
    second = api_manager.user_steps.create_account(create_user_request)
    return UserTwoAccountsContext(user=create_user_request, first=first, second=second)


@pytest.fixture
def user_two_accounts_funded(
    api_manager: ApiManager, user_two_accounts: UserTwoAccountsContext
) -> UserTwoAccountsContext:
    limits = get_limits()
    api_manager.user_steps.fund_account(
        user_two_accounts.user, user_two_accounts.first.id, limits.transfer_max
    )
    return user_two_accounts
