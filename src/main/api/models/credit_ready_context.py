from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_response import CreditResponse


class CreditReadyContext(BaseModel):
    user: CreateUserRequest
    account: CreateAccountResponse
    credit: CreditResponse
    repay_body: CreditRepayRequest
    transactions_before_repay: int
