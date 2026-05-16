from src.main.api.models.base_model import BaseModel


class CreditHistoryItem(BaseModel):
    creditId: int
    accountId: int
    balance: float


class CreditHistoryResponse(BaseModel):
    userId: int
    credits: list[CreditHistoryItem]
