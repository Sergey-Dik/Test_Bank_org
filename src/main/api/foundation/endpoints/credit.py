from src.main.api.foundation.endpoints.configuration import EndpointConfiguration
from src.main.api.models.credit_history_response import CreditHistoryResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_request_body import CreditRequestBody
from src.main.api.models.credit_response import CreditResponse


class CreditEndpoints:
    REQUEST = EndpointConfiguration(
        url="/credit/request",
        request_model=CreditRequestBody,
        response_model=CreditResponse,
    )
    REPAY = EndpointConfiguration(
        url="/credit/repay",
        request_model=CreditRepayRequest,
        response_model=CreditRepayResponse,
    )
    HISTORY = EndpointConfiguration(
        url="/credit/history",
        response_model=CreditHistoryResponse,
    )
