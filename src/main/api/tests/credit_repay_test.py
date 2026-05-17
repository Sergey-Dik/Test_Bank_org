import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_body import CreditRequestBody
from src.main.api.specs.contract_specs import ContractSpecs


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.regression
    def test_credit_repay_unauthorized(self, api_manager: ApiManager, credit_secret_user):
        _, account = credit_secret_user
        body = CreditRepayRequest(creditId=1, accountId=account.id, amount=6000.0)
        response = api_manager.user_steps.credit_repay_unauthorized(body)
        ContractSpecs.assert_error_payload(response.json())

    @pytest.mark.smoke
    def test_credit_request_and_repay(
        self,
        api_manager: ApiManager,
        credit_secret_user,
        db_session: Session,
    ):
        user, account = credit_secret_user
        api_manager.user_steps.deposit(user, account.id, 6000.0)
        credit = api_manager.user_steps.credit_request(
            user, CreditRequestBody(accountId=account.id, amount=6000.0)
        )
        repay_body = CreditRepayRequest(
            creditId=credit.creditId, accountId=account.id, amount=6000.0
        )
        transactions_before_repay = TransactionCrudDb.count_by_account_id(db_session, account.id)
        repaid = api_manager.user_steps.credit_repay(user, repay_body)
        assert repaid.amountDeposited == 6000.0
        history = api_manager.user_steps.credit_history(user)
        assert any(
            item.creditId == credit.creditId and item.balance == 0 for item in history.credits
        )
        DbAssertions.assert_credit_exists(db_session, credit.creditId)
        DbAssertions.assert_transaction_count_at_least(
            db_session, account.id, transactions_before_repay + 1
        )
