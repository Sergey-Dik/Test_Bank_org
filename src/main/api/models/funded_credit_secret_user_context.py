from __future__ import annotations

from src.main.api.models.user_account_context import UserAccountContext


class FundedCreditSecretUserContext(UserAccountContext):
    funded_amount: float

    @classmethod
    def from_user_account(
        cls, ctx: UserAccountContext, funded_amount: float
    ) -> FundedCreditSecretUserContext:
        return cls(user=ctx.user, account=ctx.account, funded_amount=funded_amount)
