import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.models.credit_request_body import CreditRequestBody


@pytest.mark.api
class TestCreditHistory:
    @pytest.mark.regression
    def test_credit_history_unauthorized(self, api_manager: ApiManager):
        api_manager.user_steps.credit_history_unauthorized()

    @pytest.mark.regression
    def test_credit_history_after_request(
        self,
        api_manager: ApiManager,
        credit_secret_user,
        db_session: Session,
    ):
        user, account = credit_secret_user
        credit = api_manager.user_steps.credit_request(
            user, CreditRequestBody(accountId=account.id, amount=6000.0)
        )
        history = api_manager.user_steps.credit_history(user)
        assert any(item.creditId == credit.creditId for item in history.credits)
        DbAssertions.assert_credit_exists(db_session, credit.creditId)
