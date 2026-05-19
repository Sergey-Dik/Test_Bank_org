from requests import Response

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests import CreateUserRequester, Requester
from src.main.api.specs.requests_specs import RequestsSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest) -> Response:
        return CreateUserRequester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok(),
        ).post(create_user_request)

    def register_created_user(self, user: CreateUserResponse) -> None:
        self.created_obj.append(user)

    def create_invalid_user(self, create_user_request: CreateUserRequest) -> Response:
        return CreateUserRequester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad(),
        ).post(create_user_request)

    def delete_user(self, user_id: int) -> Response:
        return Requester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok(),
        ).delete(user_id)

    def login_user(self, login_user_request: LoginUserRequest | CreateUserRequest) -> Response:
        if isinstance(login_user_request, CreateUserRequest):
            login_user_request = LoginUserRequest(
                username=login_user_request.username,
                password=login_user_request.password,
            )
        return Requester(
            RequestsSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_ok(),
        ).post(login_user_request)

    def list_users(self) -> Response:
        return Requester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_LIST_USERS,
            ResponseSpecs.request_ok(),
        ).get()

    def list_users_unauthorized(self) -> Response:
        return Requester(
            RequestsSpecs.unauth_headers(),
            Endpoint.ADMIN_LIST_USERS,
            ResponseSpecs.request_unauthorized(),
        ).get()
