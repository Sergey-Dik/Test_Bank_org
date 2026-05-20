import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.configs.business_limits import get_limits
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.generators.amount_generator import random_credit_amount
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.generators.test_data_strategy import with_unique_username
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_ready_context import CreditReadyContext
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_body import CreditRequestBody
from src.main.api.models.credit_two_accounts_context import CreditTwoAccountsContext
from src.main.api.models.credit_user_context import CreditUserContext
from src.main.api.models.funded_credit_secret_user_context import FundedCreditSecretUserContext
from src.main.api.models.user_account_context import UserAccountContext
from src.main.api.utils.helpers.setup_helpers import (
    setup_account,
    setup_credit_request,
    setup_fund_account,
    setup_user,
)


@pytest.fixture
def credit_secret_user(api_manager: ApiManager) -> UserAccountContext:
    user_request = with_unique_username(RandomModelGenerator.generate(CreateUserRequest))
    user_request.role = "ROLE_CREDIT_SECRET"
    setup_user(api_manager, user_request)
    account = setup_account(api_manager, user_request)
    return UserAccountContext(user=user_request, account=account)


@pytest.fixture
def funded_credit_secret_user(
    credit_secret_user: UserAccountContext, api_manager: ApiManager, request
) -> FundedCreditSecretUserContext:
    amount = request.param
    setup_fund_account(
        api_manager, credit_secret_user.user, credit_secret_user.account.id, amount
    )
    return FundedCreditSecretUserContext.from_user_account(credit_secret_user, amount)


@pytest.fixture
def credit_secret_user_funded_min(
    credit_secret_user: UserAccountContext, api_manager: ApiManager
) -> UserAccountContext:
    limits = get_limits()
    setup_fund_account(
        api_manager, credit_secret_user.user, credit_secret_user.account.id, limits.credit_min
    )
    return credit_secret_user


@pytest.fixture
def credit_secret_user_with_credit(
    credit_secret_user: UserAccountContext, api_manager: ApiManager
) -> CreditUserContext:
    amount = random_credit_amount()
    credit = setup_credit_request(
        api_manager,
        credit_secret_user.user,
        CreditRequestBody(accountId=credit_secret_user.account.id, amount=amount, termMonths=12),
    )
    return CreditUserContext.from_user_account(credit_secret_user, credit)


@pytest.fixture
def credit_secret_two_accounts_with_credit(
    credit_secret_user: UserAccountContext, api_manager: ApiManager
) -> CreditTwoAccountsContext:
    second_account = setup_account(api_manager, credit_secret_user.user)
    amount = random_credit_amount()
    credit = setup_credit_request(
        api_manager,
        credit_secret_user.user,
        CreditRequestBody(accountId=credit_secret_user.account.id, amount=amount, termMonths=12),
    )
    return CreditTwoAccountsContext(
        user=credit_secret_user.user,
        first_account=credit_secret_user.account,
        second_account=second_account,
        credit=credit,
    )


@pytest.fixture
def credit_ready_for_repay(
    credit_secret_user: UserAccountContext,
    api_manager: ApiManager,
    db_session: Session,
) -> CreditReadyContext:
    amount = random_credit_amount()
    setup_fund_account(api_manager, credit_secret_user.user, credit_secret_user.account.id, amount)
    credit = setup_credit_request(
        api_manager,
        credit_secret_user.user,
        CreditRequestBody(accountId=credit_secret_user.account.id, amount=amount, termMonths=12),
    )
    repay_body = CreditRepayRequest(
        creditId=credit.creditId,
        accountId=credit_secret_user.account.id,
        amount=amount,
    )
    transactions_before_repay = TransactionCrudDb.count_by_account_id(
        db_session, credit_secret_user.account.id
    )
    return CreditReadyContext(
        user=credit_secret_user.user,
        account=credit_secret_user.account,
        credit=credit,
        repay_body=repay_body,
        transactions_before_repay=transactions_before_repay,
    )
