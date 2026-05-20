import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.generators.amount_generator import random_credit_amount
from src.main.api.models.credit_history_response import CreditHistoryResponse
from src.main.api.models.credit_ready_context import CreditReadyContext
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.user_account_context import UserAccountContext
from src.main.api.utils.helpers.api_assertions import assert_ok_model, assert_unauthorized


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.regression
    def test_credit_repay_unauthorized(
        self, api_manager: ApiManager, credit_secret_user: UserAccountContext
    ):
        body = CreditRepayRequest(
            creditId=1,
            accountId=credit_secret_user.account.id,
            amount=random_credit_amount(),
        )
        response = api_manager.user_steps.credit_repay_unauthorized(body)
        assert_unauthorized(response)

    @pytest.mark.smoke
    def test_credit_request_and_repay(
        self,
        api_manager: ApiManager,
        credit_ready_for_repay: CreditReadyContext,
        db_session: Session,
    ):
        ctx = credit_ready_for_repay
        repay_response = api_manager.user_steps.credit_repay(ctx.user, ctx.repay_body)
        repaid = assert_ok_model(repay_response, CreditRepayResponse)
        assert repaid.amountDeposited == ctx.repay_body.amount, (
            "Repay should deposit the full credit amount"
        )
        history_response = api_manager.user_steps.credit_history(ctx.user)
        history = assert_ok_model(history_response, CreditHistoryResponse)
        credit_in_history = next(
            (item for item in history.credits if item.creditId == ctx.credit.creditId),
            None,
        )
        assert credit_in_history is not None, (
            f"Credit {ctx.credit.creditId} not found in history"
        )
        assert credit_in_history.balance == 0, (
            f"Expected zero balance after repay, got {credit_in_history.balance}"
        )
        DbAssertions.assert_credit_exists(db_session, ctx.credit.creditId)
        DbAssertions.assert_transaction_count_at_least(
            db_session, ctx.account.id, ctx.transactions_before_repay + 1
        )
