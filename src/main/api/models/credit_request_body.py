from src.main.api.models.base_model import BaseModel


class CreditRequestBody(BaseModel):
    accountId: int
    amount: float
    termMonths: int = 12
