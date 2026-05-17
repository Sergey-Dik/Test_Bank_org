import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.configs.business_limits import get_limits
from src.main.api.db.assertions import DbAssertions
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.contract_specs import ContractSpecs

_LIMITS = get_limits()


@pytest.mark.api
class TestTransferAccount:
    @pytest.mark.smoke
    def test_transfer_account(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_two_accounts,
    ):
        first, second = user_two_accounts
        api_manager.user_steps.deposit(create_user_request, first.id, 5000.0)
        amount = 1000.0
        api_manager.user_steps.transfer(create_user_request, first.id, second.id, amount)
        DbAssertions.assert_account_balance(db_session, second.id, amount)

    @pytest.mark.regression
    @pytest.mark.parametrize("amount", [_LIMITS.transfer_min, _LIMITS.transfer_max])
    def test_transfer_account_boundary_success(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_two_accounts,
        amount: float,
    ):
        first, second = user_two_accounts
        api_manager.user_steps.fund_account(create_user_request, first.id, _LIMITS.transfer_max)
        api_manager.user_steps.transfer(create_user_request, first.id, second.id, amount)
        DbAssertions.assert_account_balance(db_session, second.id, amount)

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "amount",
        [_LIMITS.transfer_min - 1, _LIMITS.transfer_max + 1],
    )
    def test_transfer_account_boundary_invalid(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_two_accounts,
        amount: float,
    ):
        first, second = user_two_accounts
        api_manager.user_steps.fund_account(create_user_request, first.id, _LIMITS.transfer_max)
        before = second.balance
        response = api_manager.user_steps.transfer_expect_bad(
            create_user_request, first.id, second.id, amount
        )
        ContractSpecs.assert_error_payload(response.json())
        DbAssertions.assert_account_balance(db_session, second.id, before)

    @pytest.mark.regression
    def test_transfer_account_unauthorized(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_two_accounts,
    ):
        first, second = user_two_accounts
        api_manager.user_steps.fund_account(create_user_request, first.id, _LIMITS.transfer_min)
        before = second.balance
        response = api_manager.user_steps.transfer_unauthorized(
            first.id, second.id, _LIMITS.transfer_min
        )
        ContractSpecs.assert_error_payload(response.json())
        DbAssertions.assert_account_balance(db_session, second.id, before)
