from src.main.api.fixtures.account_fixture import (
    user_first_account,
    user_two_accounts,
    user_two_accounts_funded,
)
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.fixtures.credit_fixture import (
    credit_ready_for_repay,
    credit_secret_two_accounts_with_credit,
    credit_secret_user,
    credit_secret_user_funded_min,
    credit_secret_user_with_credit,
    funded_credit_secret_user,
)
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.fixtures.http_fixture import http_context
from src.main.api.fixtures.object_fixture import created_obj
from src.main.api.fixtures.user_fixture import create_user_request
from src.main.api.foundation.http_context import get_http_context

__all__ = [
    "api_manager",
    "created_obj",
    "create_user_request",
    "credit_ready_for_repay",
    "credit_secret_two_accounts_with_credit",
    "credit_secret_user",
    "credit_secret_user_funded_min",
    "credit_secret_user_with_credit",
    "db_session",
    "funded_credit_secret_user",
    "http_context",
    "user_first_account",
    "user_two_accounts",
    "user_two_accounts_funded",
]


def pytest_runtest_setup(item):
    try:
        get_http_context().clear_last_exchange()
    except Exception:
        pass
