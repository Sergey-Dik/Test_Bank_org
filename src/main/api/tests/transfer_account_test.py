import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.generators.test_data_strategy import with_unique_username
from src.main.api.models.create_user_request import CreateUserRequest


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
    @pytest.mark.parametrize("amount", [500.0, 10000.0])
    def test_transfer_account_boundary_success(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_two_accounts,
        amount: float,
    ):
        first, second = user_two_accounts
        api_manager.user_steps.fund_account(create_user_request, first.id, 10000.0)
        api_manager.user_steps.transfer(create_user_request, first.id, second.id, amount)
        DbAssertions.assert_account_balance(db_session, second.id, amount)

    @pytest.mark.regression
    @pytest.mark.parametrize("amount", [499.0, 10001.0])
    def test_transfer_account_boundary_invalid(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_two_accounts,
        amount: float,
    ):
        first, second = user_two_accounts
        api_manager.user_steps.fund_account(create_user_request, first.id, 10000.0)
        before = second.balance
        api_manager.user_steps.transfer_expect_bad(
            create_user_request, first.id, second.id, amount
        )
        DbAssertions.assert_account_balance(db_session, second.id, before)

    @pytest.mark.regression
    def test_transfer_to_another_user_account(
        self,
        db_session: Session,
        api_manager: ApiManager,
    ):
        sender = with_unique_username(RandomModelGenerator.generate(CreateUserRequest))
        api_manager.admin_steps.create_user(sender)
        sender_account = api_manager.user_steps.create_account(sender)
        api_manager.user_steps.deposit(sender, sender_account.id, 5000.0)

        recipient = with_unique_username(RandomModelGenerator.generate(CreateUserRequest))
        api_manager.admin_steps.create_user(recipient)
        recipient_account = api_manager.user_steps.create_account(recipient)

        amount = 1000.0
        api_manager.user_steps.transfer(
            sender, sender_account.id, recipient_account.id, amount
        )
        DbAssertions.assert_account_balance(db_session, recipient_account.id, amount)

    @pytest.mark.regression
    def test_transfer_account_unauthorized(
        self,
        db_session: Session,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_two_accounts,
    ):
        first, second = user_two_accounts
        api_manager.user_steps.fund_account(create_user_request, first.id, 500.0)
        before = second.balance
        api_manager.user_steps.transfer_unauthorized(first.id, second.id, 500.0)
        DbAssertions.assert_account_balance(db_session, second.id, before)
