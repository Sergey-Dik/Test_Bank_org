from src.main.api.foundation.api_url import build_api_url
from src.main.api.foundation.http_context import get_http_context
from src.main.api.foundation.requesters.requester_allure import (
    attach_request_details,
    attach_response_details,
    http_request_step,
)
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestsSpecs:
    @staticmethod
    def base_headers() -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "accept": "application/json",
        }

    @staticmethod
    def auth_headers(username: str, password: str) -> dict[str, str]:
        context = get_http_context()
        cached = context.get_token(username, password)
        if cached:
            headers = RequestsSpecs.base_headers()
            headers["Authorization"] = f"Bearer {cached}"
            return headers

        request = LoginUserRequest(username=username, password=password)
        url = build_api_url("/auth/token/login")
        body = request.model_dump()
        headers = RequestsSpecs.base_headers()

        with http_request_step("POST", url):
            attach_request_details(headers, body)
            response = context.session.post(url=url, json=body, headers=headers)
            attach_response_details(response)

        if response.status_code != 200:
            raise RuntimeError(f"Failed to login as {username}: {response.text}")

        token = LoginUserResponse.model_validate(response.json()).token
        context.cache_token(username, password, token)
        auth_headers = RequestsSpecs.base_headers()
        auth_headers["Authorization"] = f"Bearer {token}"
        return auth_headers

    @staticmethod
    def unauth_headers() -> dict[str, str]:
        return RequestsSpecs.base_headers()
