import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.assertions import DbAssertions
from src.main.api.generators.amount_generator import random_deposit_amount, random_transfer_amount
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.generators.test_data_strategy import with_unique_username
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_two_accounts_context import UserTwoAccountsContext


@pytest.mark.api
class TestTransferAccount:
    @pytest.mark.smoke
    def test_transfer_account(
        self,
        db_session: Session,
        api_manager: ApiManager,
        user_two_accounts_funded: UserTwoAccountsContext,
    ):
        ctx = user_two_accounts_funded
        amount = random_transfer_amount()
        api_manager.user_steps.transfer(ctx.user, ctx.first.id, ctx.second.id, amount)
        DbAssertions.assert_account_balance(db_session, ctx.second.id, amount)

    @pytest.mark.regression
    @pytest.mark.parametrize("amount", [500.0, 10000.0])
    def test_transfer_account_boundary_success(
        self,
        db_session: Session,
        api_manager: ApiManager,
        user_two_accounts_funded: UserTwoAccountsContext,
        amount: float,
    ):
        ctx = user_two_accounts_funded
        api_manager.user_steps.transfer(ctx.user, ctx.first.id, ctx.second.id, amount)
        DbAssertions.assert_account_balance(db_session, ctx.second.id, amount)

    @pytest.mark.regression
    @pytest.mark.parametrize("amount", [499.0, 10001.0])
    def test_transfer_account_boundary_invalid(
        self,
        db_session: Session,
        api_manager: ApiManager,
        user_two_accounts_funded: UserTwoAccountsContext,
        amount: float,
    ):
        ctx = user_two_accounts_funded
        before = ctx.second.balance
        api_manager.user_steps.transfer_expect_bad(ctx.user, ctx.first.id, ctx.second.id, amount)
        DbAssertions.assert_account_balance(db_session, ctx.second.id, before)

    @pytest.mark.regression
    def test_transfer_to_another_user_account(
        self,
        db_session: Session,
        api_manager: ApiManager,
    ):
        sender = with_unique_username(RandomModelGenerator.generate(CreateUserRequest))
        api_manager.admin_steps.create_user(sender)
        sender_account = api_manager.user_steps.create_account(sender)
        api_manager.user_steps.deposit(sender, sender_account.id, random_deposit_amount())

        recipient = with_unique_username(RandomModelGenerator.generate(CreateUserRequest))
        api_manager.admin_steps.create_user(recipient)
        recipient_account = api_manager.user_steps.create_account(recipient)

        amount = random_transfer_amount()
        api_manager.user_steps.transfer(sender, sender_account.id, recipient_account.id, amount)
        DbAssertions.assert_account_balance(db_session, recipient_account.id, amount)

    @pytest.mark.regression
    def test_transfer_account_unauthorized(
        self,
        db_session: Session,
        api_manager: ApiManager,
        user_two_accounts_funded: UserTwoAccountsContext,
    ):
        ctx = user_two_accounts_funded
        before = ctx.second.balance
        api_manager.user_steps.transfer_unauthorized(
            ctx.first.id, ctx.second.id, random_transfer_amount()
        )
        DbAssertions.assert_account_balance(db_session, ctx.second.id, before)
