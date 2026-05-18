from __future__ import annotations

from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.user_account_context import UserAccountContext


class CreditUserContext(UserAccountContext):
    credit: CreditResponse

    @classmethod
    def from_user_account(
        cls, ctx: UserAccountContext, credit: CreditResponse
    ) -> CreditUserContext:
        return cls(user=ctx.user, account=ctx.account, credit=credit)
