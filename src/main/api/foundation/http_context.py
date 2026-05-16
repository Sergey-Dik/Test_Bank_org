from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class HttpExchange:
    method: str
    url: str
    request_headers: dict[str, Any]
    request_body: Any
    status_code: int
    response_body: Any


class HttpContext:
    def __init__(self) -> None:
        self.session = requests.Session()
        self._tokens: dict[tuple[str, str], str] = {}
        self.last_exchange: HttpExchange | None = None

    def cache_token(self, username: str, password: str, token: str) -> None:
        self._tokens[(username, password)] = token

    def get_token(self, username: str, password: str) -> str | None:
        return self._tokens.get((username, password))

    def clear_last_exchange(self) -> None:
        self.last_exchange = None


_context: HttpContext | None = None


def get_http_context() -> HttpContext:
    global _context
    if _context is None:
        _context = HttpContext()
    return _context
