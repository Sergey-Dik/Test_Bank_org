"""Precondition setup for fixtures (uses same checks as tests)."""

from src.main.api.classes.api_manager import ApiManager
from src.main.api.configs.business_limits import get_limits
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_request_body import CreditRequestBody
from src.main.api.models.credit_response import CreditResponse
from src.main.api.utils.api_assertions import (
    assert_created_model,
    assert_ok,
    assert_ok_model,
)


def setup_user(api_manager: ApiManager, user_request: CreateUserRequest) -> CreateUserResponse:
    response = api_manager.admin_steps.create_user(user_request)
    user = assert_ok_model(response, CreateUserResponse)
    api_manager.admin_steps.register_created_user(user)
    return user


def setup_account(api_manager: ApiManager, user: CreateUserRequest) -> CreateAccountResponse:
    response = api_manager.user_steps.create_account(user)
    return assert_created_model(response, CreateAccountResponse)


def setup_fund_account(
    api_manager: ApiManager, user: CreateUserRequest, account_id: int, target_amount: float
) -> None:
    limits = get_limits()
    remaining = target_amount
    while remaining > 0:
        chunk = min(remaining, limits.deposit_max)
        if chunk < limits.deposit_min:
            chunk = limits.deposit_min
        response = api_manager.user_steps.deposit(user, account_id, chunk)
        assert_ok(response)
        remaining -= chunk


def setup_credit_request(
    api_manager: ApiManager, user: CreateUserRequest, body: CreditRequestBody
) -> CreditResponse:
    response = api_manager.user_steps.credit_request(user, body)
    return assert_created_model(response, CreditResponse)
