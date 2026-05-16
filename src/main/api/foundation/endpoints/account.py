from src.main.api.foundation.endpoints.configuration import EndpointConfiguration
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest


class AccountEndpoints:
    CREATE = EndpointConfiguration(
        url="/account/create",
        response_model=CreateAccountResponse,
    )
    DEPOSIT = EndpointConfiguration(
        url="/account/deposit",
        request_model=DepositRequest,
        response_model=CreateAccountResponse,
    )
    TRANSFER = EndpointConfiguration(
        url="/account/transfer",
        request_model=TransferRequest,
        response_model=None,
    )
