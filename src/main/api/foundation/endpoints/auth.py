from src.main.api.foundation.endpoints.configuration import EndpointConfiguration
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class AuthEndpoints:
    LOGIN = EndpointConfiguration(
        url="/auth/token/login",
        request_model=LoginUserRequest,
        response_model=LoginUserResponse,
    )
