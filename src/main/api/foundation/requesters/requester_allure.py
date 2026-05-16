from __future__ import annotations

import json
from typing import Any

import allure
from requests import Response


def http_request_step(method: str, url: str):
    return allure.step(f"HTTP {method} {url}")


def attach_request_details(headers: dict[str, Any] | None, body: Any = None) -> None:
    if headers:
        allure.attach(
            json.dumps(headers, ensure_ascii=False, indent=2),
            name="request headers",
            attachment_type=allure.attachment_type.JSON,
        )
    if body is not None and body != "":
        payload = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False, indent=2)
        allure.attach(payload, name="request body", attachment_type=allure.attachment_type.JSON)


def attach_response_details(response: Response) -> None:
    try:
        body = response.json()
        payload = json.dumps(body, ensure_ascii=False, indent=2)
    except Exception:
        payload = response.text
    allure.attach(
        payload,
        name=f"response {response.status_code}",
        attachment_type=allure.attachment_type.JSON,
    )


def attach_validated_model(model: Any) -> None:
    allure.attach(
        model.model_dump_json(indent=2),
        name="validated model",
        attachment_type=allure.attachment_type.JSON,
    )
