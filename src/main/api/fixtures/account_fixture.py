import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.configs.business_limits import get_limits
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_two_accounts_context import UserTwoAccountsContext
from src.main.api.tests.setup_helpers import setup_account, setup_fund_account


@pytest.fixture
def user_first_account(api_manager: ApiManager, create_user_request: CreateUserRequest):
    return setup_account(api_manager, create_user_request)


@pytest.fixture
def user_two_accounts(
    api_manager: ApiManager, create_user_request: CreateUserRequest
) -> UserTwoAccountsContext:
    first = setup_account(api_manager, create_user_request)
    second = setup_account(api_manager, create_user_request)
    return UserTwoAccountsContext(user=create_user_request, first=first, second=second)


@pytest.fixture
def user_two_accounts_funded(
    api_manager: ApiManager, user_two_accounts: UserTwoAccountsContext
) -> UserTwoAccountsContext:
    limits = get_limits()
    setup_fund_account(
        api_manager, user_two_accounts.user, user_two_accounts.first.id, limits.transfer_max
    )
    return user_two_accounts
