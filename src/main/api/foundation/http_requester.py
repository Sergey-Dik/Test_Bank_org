from collections.abc import Callable
from typing import Any

from src.main.api.foundation.crud_endpoint import CrudEndpoint


class HttpRequester:
    def __init__(
        self,
        request_spec: dict[str, str],
        endpoint: CrudEndpoint,
        response_spec: Callable[..., Any],
    ):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec
