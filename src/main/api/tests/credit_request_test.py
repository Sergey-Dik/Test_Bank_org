import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.generators.amount_generator import random_credit_amount
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_body import CreditRequestBody
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.funded_credit_secret_user_context import FundedCreditSecretUserContext
from src.main.api.models.user_account_context import UserAccountContext
from src.main.api.utils.api_assertions import (
    assert_bad_request,
    assert_created_model,
    assert_forbidden,
    assert_not_found,
    assert_unauthorized,
)


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.smoke
    def test_credit_request_success(
        self,
        db_session: Session,
        api_manager: ApiManager,
        credit_secret_user: UserAccountContext,
    ):
        amount = random_credit_amount()
        body = CreditRequestBody(
            accountId=credit_secret_user.account.id, amount=amount, termMonths=12
        )
        response = api_manager.user_steps.credit_request(credit_secret_user.user, body)
        credit = assert_created_model(response, CreditResponse)
        assert credit.creditId > 0, "Credit id should be positive"
        DbAssertions.assert_credit_exists(db_session, credit.creditId)

    @pytest.mark.regression
    def test_credit_request_unauthorized(self, api_manager: ApiManager, user_first_account):
        body = CreditRequestBody(accountId=user_first_account.id, amount=random_credit_amount())
        response = api_manager.user_steps.credit_request_unauthorized(body)
        assert_unauthorized(response)

    @pytest.mark.regression
    def test_credit_request_forbidden_for_role_user(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_first_account,
    ):
        body = CreditRequestBody(accountId=user_first_account.id, amount=random_credit_amount())
        response = api_manager.user_steps.credit_request_forbidden(create_user_request, body)
        assert_forbidden(response)

    @pytest.mark.regression
    def test_second_credit_on_other_account_not_allowed(
        self,
        db_session: Session,
        api_manager: ApiManager,
        credit_secret_two_accounts_with_credit,
    ):
        ctx = credit_secret_two_accounts_with_credit
        response = api_manager.user_steps.request_credit_on_second_account_expect_not_found(
            ctx.user, ctx.second_account.id, random_credit_amount()
        )
        assert_not_found(response)
        assert CreditCrudDb.count_by_account_id(db_session, ctx.second_account.id) == 0, (
            "Second account must not have a credit record"
        )

    @pytest.mark.regression
    @pytest.mark.parametrize("funded_credit_secret_user", [5000.0, 15000.0], indirect=True)
    def test_credit_request_boundary_success(
        self,
        db_session: Session,
        api_manager: ApiManager,
        funded_credit_secret_user: FundedCreditSecretUserContext,
    ):
        ctx = funded_credit_secret_user
        body = CreditRequestBody(accountId=ctx.account.id, amount=ctx.funded_amount, termMonths=12)
        response = api_manager.user_steps.credit_request(ctx.user, body)
        credit = assert_created_model(response, CreditResponse)
        assert credit.creditId > 0, "Credit id should be positive"
        DbAssertions.assert_credit_exists(db_session, credit.creditId)

    @pytest.mark.regression
    @pytest.mark.parametrize("amount", [4999.0, 15001.0])
    def test_credit_request_boundary_invalid(
        self,
        db_session: Session,
        api_manager: ApiManager,
        credit_secret_user_funded_min: UserAccountContext,
        amount: float,
    ):
        ctx = credit_secret_user_funded_min
        before = CreditCrudDb.count_by_account_id(db_session, ctx.account.id)
        response = api_manager.user_steps.credit_request_expect_bad(
            ctx.user, ctx.account.id, amount
        )
        assert_bad_request(response)
        assert CreditCrudDb.count_by_account_id(db_session, ctx.account.id) == before, (
            "Invalid credit request must not create a credit record"
        )
