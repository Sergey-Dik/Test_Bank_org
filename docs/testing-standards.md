# Testing standards

## Layers

`tests -> fixtures -> ApiManager -> Steps -> Requesters -> build_api_url / Endpoint -> backend`

Схема: `../Full description of the framework projects/Test_Bank_Architecture.html`

## Data isolation

- `with_unique_username(...)` for new users
- `fund_account(...)` when deposit per operation is limited — uses `get_limits()` from `configs/business_limits.py`

## Business limits

- Defaults: deposit 1000–9000, transfer 500–10000, credit 5000–15000
- Override keys in `urls.properties`: `deposit.min`, `deposit.max`, etc.

## DB checks

- Models aligned with PostgreSQL: `user`, `account`, `credit`, `transaction`
- `transaction_type`, `to_account_id`, `from_account_id`
- Use `DbAssertions` / CRUD, not raw SQL

## Contracts

- `ContractSpecs` on negative API responses
- Separate Pydantic models per API shape (e.g. `CreditRepayResponse`)

## CI gates

- `ruff check src conftest.py scripts`
- `pytest` and `pytest -n auto --dist=loadscope` — 40 tests
