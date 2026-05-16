from sqlalchemy.orm import Session

from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.db.crud.user_crud import UserCrudDb


class DbAssertions:
    @staticmethod
    def assert_user_exists(db: Session, username: str) -> None:
        user = UserCrudDb.get_user_by_username(db, username)
        assert user is not None, f"User {username} not found in DB"

    @staticmethod
    def assert_user_not_exists(db: Session, username: str) -> None:
        user = UserCrudDb.get_user_by_username(db, username)
        assert user is None, f"User {username} should not exist in DB"

    @staticmethod
    def assert_account_exists(db: Session, account_id: int) -> None:
        account = AccountCrudDb.get_account_by_id(db, account_id)
        assert account is not None, f"Account {account_id} not found in DB"

    @staticmethod
    def assert_account_balance(db: Session, account_id: int, expected: float) -> None:
        account = AccountCrudDb.get_account_by_id(db, account_id)
        assert account is not None
        assert account.balance == expected

    @staticmethod
    def assert_credit_exists(db: Session, credit_id: int) -> None:
        credit = CreditCrudDb.get_by_credit_id(db, credit_id)
        assert credit is not None, f"Credit {credit_id} not found in DB"

    @staticmethod
    def assert_transaction_count_at_least(
        db: Session, account_id: int, minimum: int, tx_type: str | None = None
    ) -> None:
        if tx_type:
            count = TransactionCrudDb.count_by_account_and_type(db, account_id, tx_type)
        else:
            count = TransactionCrudDb.count_by_account_id(db, account_id)
        assert count >= minimum, f"Expected at least {minimum} transactions, got {count}"
