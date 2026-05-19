from requests import Response

from src.main.api.configs.business_limits import get_limits
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_body import CreditRequestBody
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.requests import (
    CreateAccountRequester,
    DepositRequester,
    LoginUserRequester,
    Requester,
    TransferRequester,
)
from src.main.api.specs.requests_specs import RequestsSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def _user_headers(self, user: CreateUserRequest) -> dict[str, str]:
        return RequestsSpecs.auth_headers(user.username, user.password)

    def create_account(self, user: CreateUserRequest) -> Response:
        return CreateAccountRequester(
            self._user_headers(user),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created(),
        ).post()

    def create_account_as_admin_expect_forbidden(self) -> Response:
        return CreateAccountRequester(
            RequestsSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_forbidden(),
        ).post()

    def create_account_expect_conflict(self, user: CreateUserRequest) -> Response:
        return CreateAccountRequester(
            self._user_headers(user),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_conflict(),
        ).post()

    def fund_account(self, user: CreateUserRequest, account_id: int, target_amount: float) -> None:
        limits = get_limits()
        remaining = target_amount
        while remaining > 0:
            chunk = min(remaining, limits.deposit_max)
            if chunk < limits.deposit_min:
                chunk = limits.deposit_min
            self.deposit(user, account_id, chunk)
            remaining -= chunk

    def deposit(self, user: CreateUserRequest, account_id: int, amount: float) -> Response:
        body = DepositRequest(accountId=account_id, amount=amount)
        return DepositRequester(
            self._user_headers(user),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok(),
        ).post(body)

    def deposit_expect_bad(
        self, user: CreateUserRequest, account_id: int, amount: float
    ) -> Response:
        body = DepositRequest(accountId=account_id, amount=amount)
        return DepositRequester(
            self._user_headers(user),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_bad(),
        ).post(body)

    def deposit_unauthorized(self, account_id: int, amount: float) -> Response:
        body = DepositRequest(accountId=account_id, amount=amount)
        return DepositRequester(
            RequestsSpecs.unauth_headers(),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_unauthorized(),
        ).post(body)

    def transfer(
        self,
        user: CreateUserRequest,
        from_account_id: int,
        to_account_id: int,
        amount: float,
    ) -> Response:
        body = TransferRequest(
            fromAccountId=from_account_id,
            toAccountId=to_account_id,
            amount=amount,
        )
        return TransferRequester(
            self._user_headers(user),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok(),
        ).post(body)

    def transfer_expect_bad(
        self,
        user: CreateUserRequest,
        from_account_id: int,
        to_account_id: int,
        amount: float,
    ) -> Response:
        body = TransferRequest(
            fromAccountId=from_account_id,
            toAccountId=to_account_id,
            amount=amount,
        )
        return TransferRequester(
            self._user_headers(user),
            Endpoint.TRANSFER,
            ResponseSpecs.request_bad(),
        ).post(body)

    def transfer_unauthorized(
        self, from_account_id: int, to_account_id: int, amount: float
    ) -> Response:
        body = TransferRequest(
            fromAccountId=from_account_id,
            toAccountId=to_account_id,
            amount=amount,
        )
        return TransferRequester(
            RequestsSpecs.unauth_headers(),
            Endpoint.TRANSFER,
            ResponseSpecs.request_unauthorized(),
        ).post(body)

    def credit_request(self, user: CreateUserRequest, body: CreditRequestBody) -> Response:
        return Requester(
            self._user_headers(user),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created(),
        ).post(body)

    def credit_request_unauthorized(self, body: CreditRequestBody) -> Response:
        return Requester(
            RequestsSpecs.unauth_headers(),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_unauthorized(),
        ).post(body)

    def credit_request_forbidden(
        self, user: CreateUserRequest, body: CreditRequestBody
    ) -> Response:
        return Requester(
            self._user_headers(user),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_forbidden(),
        ).post(body)

    def credit_request_not_found(
        self, user: CreateUserRequest, body: CreditRequestBody
    ) -> Response:
        return Requester(
            self._user_headers(user),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_not_found(),
        ).post(body)

    def credit_request_expect_bad(
        self, user: CreateUserRequest, account_id: int, amount: float
    ) -> Response:
        body = CreditRequestBody(accountId=account_id, amount=amount)
        return Requester(
            self._user_headers(user),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_bad(),
        ).post(body)

    def request_credit_on_second_account_expect_not_found(
        self, user: CreateUserRequest, second_account_id: int, amount: float
    ) -> Response:
        body = CreditRequestBody(accountId=second_account_id, amount=amount)
        return self.credit_request_not_found(user, body)

    def credit_repay(self, user: CreateUserRequest, body: CreditRepayRequest) -> Response:
        return Requester(
            self._user_headers(user),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok(),
        ).post(body)

    def credit_repay_unauthorized(self, body: CreditRepayRequest) -> Response:
        return Requester(
            RequestsSpecs.unauth_headers(),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unauthorized(),
        ).post(body)

    def credit_history(self, user: CreateUserRequest) -> Response:
        return Requester(
            self._user_headers(user),
            Endpoint.CREDIT_HISTORY,
            ResponseSpecs.request_ok(),
        ).get()

    def credit_history_unauthorized(self) -> Response:
        return Requester(
            RequestsSpecs.unauth_headers(),
            Endpoint.CREDIT_HISTORY,
            ResponseSpecs.request_unauthorized(),
        ).get()

    def login_invalid(self, login_request: LoginUserRequest) -> Response:
        return LoginUserRequester(
            RequestsSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_unauthorized(),
        ).post(login_request)
