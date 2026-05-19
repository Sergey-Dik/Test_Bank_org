import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.models.credit_history_response import CreditHistoryResponse
from src.main.api.models.credit_user_context import CreditUserContext
from src.main.api.tests.api_assertions import assert_ok_model, assert_unauthorized


@pytest.mark.api
class TestCreditHistory:
    @pytest.mark.regression
    def test_credit_history_unauthorized(self, api_manager: ApiManager):
        response = api_manager.user_steps.credit_history_unauthorized()
        assert_unauthorized(response)

    @pytest.mark.regression
    def test_credit_history_after_request(
        self,
        api_manager: ApiManager,
        credit_secret_user_with_credit: CreditUserContext,
        db_session: Session,
    ):
        ctx = credit_secret_user_with_credit
        history_response = api_manager.user_steps.credit_history(ctx.user)
        history = assert_ok_model(history_response, CreditHistoryResponse)
        credit_in_history = next(
            (item for item in history.credits if item.creditId == ctx.credit.creditId),
            None,
        )
        assert credit_in_history is not None, (
            f"Credit {ctx.credit.creditId} not found in history"
        )
        DbAssertions.assert_credit_exists(db_session, ctx.credit.creditId)
