"""Facade: re-exports endpoint configurations for steps and requesters."""

from src.main.api.foundation.endpoints.account import AccountEndpoints
from src.main.api.foundation.endpoints.admin import AdminEndpoints
from src.main.api.foundation.endpoints.auth import AuthEndpoints
from src.main.api.foundation.endpoints.configuration import EndpointConfiguration
from src.main.api.foundation.endpoints.credit import CreditEndpoints


class Endpoint:
    ADMIN_CREATE_USER = AdminEndpoints.CREATE_USER
    ADMIN_DELETE_USER = AdminEndpoints.DELETE_USER
    ADMIN_LIST_USERS = AdminEndpoints.LIST_USERS
    LOGIN_USER = AuthEndpoints.LOGIN
    CREATE_ACCOUNT = AccountEndpoints.CREATE
    DEPOSIT = AccountEndpoints.DEPOSIT
    TRANSFER = AccountEndpoints.TRANSFER
    CREDIT_REQUEST = CreditEndpoints.REQUEST
    CREDIT_REPAY = CreditEndpoints.REPAY
    CREDIT_HISTORY = CreditEndpoints.HISTORY


__all__ = ["Endpoint", "EndpointConfiguration"]
