import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.utils.helpers.api_assertions import (
    assert_conflict,
    assert_created_model,
    assert_forbidden,
)


@pytest.mark.api
class TestCreateAccount:
    @pytest.mark.smoke
    def test_create_account(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
    ):
        response = api_manager.user_steps.create_account(create_user_request)
        account = assert_created_model(response, CreateAccountResponse)
        assert account.balance == 0, "New account balance should be zero"
        assert account.id > 0, "Account id should be positive"
        assert account.number, "Account number should be present"
        DbAssertions.assert_account_exists(db_session, account.id)

    @pytest.mark.regression
    def test_admin_cannot_create_bank_account(self, api_manager: ApiManager):
        response = api_manager.user_steps.create_account_as_admin_expect_forbidden()
        assert_forbidden(response)

    @pytest.mark.regression
    def test_max_two_accounts_per_user(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
    ):
        first_response = api_manager.user_steps.create_account(create_user_request)
        first = assert_created_model(first_response, CreateAccountResponse)
        second_response = api_manager.user_steps.create_account(create_user_request)
        second = assert_created_model(second_response, CreateAccountResponse)
        conflict_response = api_manager.user_steps.create_account_expect_conflict(
            create_user_request
        )
        assert_conflict(conflict_response)
        DbAssertions.assert_account_exists(db_session, first.id)
        DbAssertions.assert_account_exists(db_session, second.id)
