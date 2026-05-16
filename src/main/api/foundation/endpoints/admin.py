from src.main.api.foundation.endpoints.configuration import EndpointConfiguration
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse


class AdminEndpoints:
    CREATE_USER = EndpointConfiguration(
        url="/admin/create",
        request_model=CreateUserRequest,
        response_model=CreateUserResponse,
    )
    DELETE_USER = EndpointConfiguration(url="/admin/users", response_model=None)
    LIST_USERS = EndpointConfiguration(url="/admin/users", response_model=None)
