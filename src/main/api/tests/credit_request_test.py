import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.configs.business_limits import get_limits
from src.main.api.db.assertions import DbAssertions
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_body import CreditRequestBody
from src.main.api.specs.contract_specs import ContractSpecs

_LIMITS = get_limits()


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.smoke
    def test_credit_request_success(
        self,
        db_session: Session,
        api_manager: ApiManager,
        credit_secret_user,
    ):
        user, account = credit_secret_user
        body = CreditRequestBody(accountId=account.id, amount=6000.0, termMonths=12)
        credit = api_manager.user_steps.credit_request(user, body)
        assert credit.creditId > 0
        DbAssertions.assert_credit_exists(db_session, credit.creditId)

    @pytest.mark.regression
    def test_credit_request_unauthorized(self, api_manager: ApiManager, user_first_account):
        body = CreditRequestBody(accountId=user_first_account.id, amount=6000.0)
        response = api_manager.user_steps.credit_request_unauthorized(body)
        ContractSpecs.assert_error_payload(response.json())

    @pytest.mark.regression
    def test_credit_request_forbidden_for_role_user(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_first_account,
    ):
        body = CreditRequestBody(accountId=user_first_account.id, amount=6000.0)
        response = api_manager.user_steps.credit_request_forbidden(create_user_request, body)
        ContractSpecs.assert_error_payload(response.json())

    @pytest.mark.regression
    def test_second_credit_on_other_account_not_allowed(
        self,
        db_session: Session,
        api_manager: ApiManager,
        credit_secret_user,
    ):
        user, first_account = credit_secret_user
        second_account = api_manager.user_steps.create_account(user)
        first_body = CreditRequestBody(accountId=first_account.id, amount=6000.0)
        api_manager.user_steps.credit_request(user, first_body)
        second_body = CreditRequestBody(accountId=second_account.id, amount=7000.0)
        response = api_manager.user_steps.credit_request_not_found(user, second_body)
        ContractSpecs.assert_error_payload(response.json())
        assert CreditCrudDb.count_by_account_id(db_session, second_account.id) == 0

    @pytest.mark.regression
    @pytest.mark.parametrize("amount", [_LIMITS.credit_min, _LIMITS.credit_max])
    def test_credit_request_boundary_success(
        self,
        db_session: Session,
        api_manager: ApiManager,
        credit_secret_user,
        amount: float,
    ):
        user, account = credit_secret_user
        api_manager.user_steps.fund_account(user, account.id, amount)
        body = CreditRequestBody(accountId=account.id, amount=amount, termMonths=12)
        credit = api_manager.user_steps.credit_request(user, body)
        assert credit.creditId > 0
        DbAssertions.assert_credit_exists(db_session, credit.creditId)

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "amount",
        [_LIMITS.credit_min - 1, _LIMITS.credit_max + 1],
    )
    def test_credit_request_boundary_invalid(
        self,
        db_session: Session,
        api_manager: ApiManager,
        credit_secret_user,
        amount: float,
    ):
        user, account = credit_secret_user
        before = CreditCrudDb.count_by_account_id(db_session, account.id)
        api_manager.user_steps.fund_account(user, account.id, get_limits().credit_min)
        response = api_manager.user_steps.credit_request_expect_bad(user, account.id, amount)
        ContractSpecs.assert_error_payload(response.json())
        assert CreditCrudDb.count_by_account_id(db_session, account.id) == before
