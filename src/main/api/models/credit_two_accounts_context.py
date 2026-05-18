from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_response import CreditResponse


class CreditTwoAccountsContext(BaseModel):
    user: CreateUserRequest
    first_account: CreateAccountResponse
    second_account: CreateAccountResponse
    credit: CreditResponse
