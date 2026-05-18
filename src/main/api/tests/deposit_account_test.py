import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestDepositAccount:
    @pytest.mark.smoke
    def test_deposit_account(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_first_account: CreateAccountResponse,
    ):
        amount = 1500.0
        response = api_manager.user_steps.deposit(
            create_user_request, user_first_account.id, amount
        )
        assert response.balance == amount
        DbAssertions.assert_account_balance(db_session, user_first_account.id, amount)
        DbAssertions.assert_transaction_count_at_least(
            db_session, user_first_account.id, 1, "deposit"
        )

    @pytest.mark.regression
    def test_deposit_account_invalid(self, api_manager: ApiManager, user_first_account):
        api_manager.user_steps.deposit_unauthorized(user_first_account.id, 1500.0)

    @pytest.mark.regression
    @pytest.mark.parametrize("amount", [1000.0, 9000.0])
    def test_deposit_account_boundary_success(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_first_account: CreateAccountResponse,
        amount: float,
    ):
        response = api_manager.user_steps.deposit(
            create_user_request, user_first_account.id, amount
        )
        assert response.balance == amount
        DbAssertions.assert_account_balance(db_session, user_first_account.id, amount)

    @pytest.mark.regression
    @pytest.mark.parametrize("amount", [999.0, 9001.0])
    def test_deposit_account_boundary_invalid(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_first_account: CreateAccountResponse,
        amount: float,
    ):
        before = user_first_account.balance
        api_manager.user_steps.deposit_expect_bad(
            create_user_request, user_first_account.id, amount
        )
        DbAssertions.assert_account_balance(db_session, user_first_account.id, before)
