from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def count_by_account_id(db: Session, account_id: int) -> int:
        return (
            db.query(Transaction)
            .filter(
                (Transaction.to_account_id == account_id)
                | (Transaction.from_account_id == account_id)
            )
            .count()
        )

    @staticmethod
    def count_by_account_and_type(db: Session, account_id: int, tx_type: str) -> int:
        return (
            db.query(Transaction)
            .filter(
                Transaction.to_account_id == account_id,
                Transaction.transaction_type == tx_type,
            )
            .count()
        )
