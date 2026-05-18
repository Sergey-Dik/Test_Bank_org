from __future__ import annotations

from typing import Any, Optional

from requests import Response
from src.main.api.foundation.api_url import build_api_url
from src.main.api.foundation.crud_endpoint import CrudEndpoint
from src.main.api.foundation.http_context import HttpExchange, get_http_context
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.requester_allure import (
    attach_request_details,
    attach_response_details,
    http_request_step,
)
from src.main.api.models.base_model import BaseModel


class Requester(HttpRequester):
    def _record_exchange(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: Any,
        response: Response,
    ) -> None:
        try:
            response_body = response.json()
        except Exception:
            response_body = response.text
        get_http_context().last_exchange = HttpExchange(
            method=method,
            url=url,
            request_headers=headers,
            request_body=body,
            status_code=response.status_code,
            response_body=response_body,
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any = None,
        path_suffix: str = "",
    ) -> Response:
        endpoint: CrudEndpoint = self.endpoint
        url = build_api_url(f"{endpoint.url}{path_suffix}")
        session = get_http_context().session
        headers = self.request_spec

        with http_request_step(method, url):
            attach_request_details(headers, json_body)
            response = session.request(method, url=url, headers=headers, json=json_body)
            self._record_exchange(method, url, headers, json_body, response)
            attach_response_details(response)

        self.response_spec(response)
        return response

    def get(self, path_suffix: str = "") -> Response:
        return self._request("GET", self.endpoint.url, path_suffix=path_suffix)

    def post(self, model: Optional[BaseModel] = None) -> Response:
        body = model.model_dump() if model is not None else None
        return self._request("POST", self.endpoint.url, json_body=body)

    def delete(self, resource_id: int) -> Response:
        return self._request("DELETE", self.endpoint.url, path_suffix=f"/{resource_id}")
