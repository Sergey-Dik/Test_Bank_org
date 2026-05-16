from __future__ import annotations

from dataclasses import dataclass

from src.main.api.configs.config import Config


@dataclass(frozen=True)
class BusinessLimits:
    deposit_min: float
    deposit_max: float
    transfer_min: float
    transfer_max: float
    credit_min: float
    credit_max: float

    @classmethod
    def load(cls) -> BusinessLimits:
        def _float(key: str, default: float) -> float:
            raw = Config.fetch(key)
            return float(raw) if raw is not None else default

        return cls(
            deposit_min=_float("deposit.min", 1000),
            deposit_max=_float("deposit.max", 9000),
            transfer_min=_float("transfer.min", 500),
            transfer_max=_float("transfer.max", 10000),
            credit_min=_float("credit.min", 5000),
            credit_max=_float("credit.max", 15000),
        )


_limits: BusinessLimits | None = None


def get_limits() -> BusinessLimits:
    global _limits
    if _limits is None:
        _limits = BusinessLimits.load()
    return _limits
