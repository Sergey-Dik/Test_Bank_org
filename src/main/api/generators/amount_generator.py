import random

from src.main.api.configs.business_limits import get_limits


def _random_in_range(min_value: float, max_value: float) -> float:
    return round(random.uniform(min_value, max_value), 2)


def random_deposit_amount() -> float:
    limits = get_limits()
    return _random_in_range(limits.deposit_min, limits.deposit_max)


def random_transfer_amount() -> float:
    limits = get_limits()
    return _random_in_range(limits.transfer_min, limits.transfer_max)


def random_credit_amount() -> float:
    limits = get_limits()
    return _random_in_range(limits.credit_min, limits.credit_max)
