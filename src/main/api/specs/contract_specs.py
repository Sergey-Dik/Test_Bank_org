from __future__ import annotations

from typing import Any


class ContractSpecs:
    @staticmethod
    def assert_error_payload(payload: dict[str, Any]) -> None:
        assert isinstance(payload, dict)
        assert any(key in payload for key in ("message", "error", "detail", "title", "type")), (
            f"Unexpected error payload shape: {payload}"
        )

    @staticmethod
    def assert_credit_history_payload(payload: dict[str, Any]) -> None:
        assert isinstance(payload, dict)
        assert "userId" in payload
        assert "credits" in payload
        assert isinstance(payload["credits"], list)
