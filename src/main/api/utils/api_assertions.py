"""HTTP/API checks for tests (status, error contract, response models)."""

from typing import Any, Callable, TypeVar

from requests import Response

from src.main.api.models.base_model import BaseModel
from src.main.api.specs.contract_specs import ContractSpecs
from src.main.api.specs.response_specs import ResponseSpecs

TModel = TypeVar("TModel", bound=BaseModel)


def assert_http_status(
    response: Response,
    status_check: Callable[[], Callable[[Response], None]],
) -> None:
    status_check()(response)


def assert_error_response(
    response: Response,
    status_check: Callable[[], Callable[[Response], None]],
) -> None:
    assert_http_status(response, status_check)
    ContractSpecs.assert_error_payload(response.json())


def parse_json_model(response: Response, model_class: type[TModel]) -> TModel:
    return model_class.model_validate(response.json())


def assert_ok(response: Response) -> None:
    assert_http_status(response, ResponseSpecs.request_ok)


def assert_created(response: Response) -> None:
    assert_http_status(response, ResponseSpecs.request_created)


def assert_bad_request(response: Response) -> None:
    assert_error_response(response, ResponseSpecs.request_bad)


def assert_unauthorized(response: Response) -> None:
    assert_error_response(response, ResponseSpecs.request_unauthorized)


def assert_forbidden(response: Response) -> None:
    assert_error_response(response, ResponseSpecs.request_forbidden)


def assert_not_found(response: Response) -> None:
    assert_error_response(response, ResponseSpecs.request_not_found)


def assert_conflict(response: Response) -> None:
    assert_error_response(response, ResponseSpecs.request_conflict)


def assert_ok_model(response: Response, model_class: type[TModel]) -> TModel:
    assert_ok(response)
    return parse_json_model(response, model_class)


def assert_created_model(response: Response, model_class: type[TModel]) -> TModel:
    assert_created(response)
    return parse_json_model(response, model_class)


def assert_ok_json(response: Response) -> Any:
    assert_ok(response)
    return response.json()
