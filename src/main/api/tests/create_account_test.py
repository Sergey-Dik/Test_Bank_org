import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.models.create_user_request import CreateUserRequest


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
        assert response.balance == 0
        assert response.id > 0
        assert response.number
        DbAssertions.assert_account_exists(db_session, response.id)

    @pytest.mark.regression
    def test_admin_cannot_create_bank_account(self, api_manager: ApiManager):
        api_manager.user_steps.create_account_as_admin_expect_forbidden()

    @pytest.mark.regression
    def test_max_two_accounts_per_user(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
    ):
        first = api_manager.user_steps.create_account(create_user_request)
        second = api_manager.user_steps.create_account(create_user_request)
        api_manager.user_steps.create_account_expect_conflict(create_user_request)
        DbAssertions.assert_account_exists(db_session, first.id)
        DbAssertions.assert_account_exists(db_session, second.id)
