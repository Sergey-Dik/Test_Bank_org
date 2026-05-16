from src.main.api.models.base_model import BaseModel


class CreditResponse(BaseModel):
    id: int
    creditId: int
    balance: float
