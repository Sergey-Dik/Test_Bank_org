# Test_Bank_org

API automation framework for the bank backend: pytest, Pydantic, PostgreSQL checks, Allure in requesters.

## Prerequisites

- Python 3.12+
- Running Bank API (Swagger: `http://localhost:4111/api/swagger`)
- PostgreSQL with backend schema (`dataBaseUrl` in config)

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `resources/urls.properties.example` → `resources/urls.properties` (or edit the existing file).

```properties
backendUrl=http://localhost:4111/api
dataBaseUrl=postgresql+psycopg2://symfony:password@localhost:5432/symfony_db
```

```bash
make lint
make test
make test-parallel
make smoke
make allure-serve
```

## Tests

**40 tests** (smoke — 8). Integration tests mutate data in the shared DB; use a dedicated test database.

Business limits (deposit / transfer / credit) are defined in `src/main/api/configs/business_limits.py`
and can be overridden via `resources/urls.properties`.

## API coverage (Swagger ↔ framework)

| Swagger | Steps | Tests |
|---------|-------|-------|
| `POST /auth/token/login` | `AdminSteps.login_user` | `login_user_test` |
| `POST /admin/create` | `AdminSteps.create_user` | `create_user_test` |
| `GET /admin/users` | `AdminSteps.list_users` | `admin_list_users_test` (+ 401 without token) |
| `DELETE /admin/users/{id}` | `AdminSteps.delete_user` | teardown in `object_fixture` only |
| `POST /account/create` | `UserSteps.create_account` | `create_account_test` |
| `POST /account/deposit` | `UserSteps.deposit` | `deposit_account_test` |
| `POST /account/transfer` | `UserSteps.transfer` | `transfer_account_test` (own accounts) |
| `POST /credit/request` | `UserSteps.credit_request` | `credit_request_test` (+ amount boundaries) |
| `GET /credit/history` | `UserSteps.credit_history` | `credit_history_test` |
| `POST /credit/repay` | `UserSteps.credit_repay` | `credit_repay_test` |

## Documentation

- [Test_Bank_Org_Onboarding.md](../Full%20description%20of%20the%20framework%20projects/Test_Bank_Org_Onboarding.md)
- [Test_Bank_Architecture.html](../Full%20description%20of%20the%20framework%20projects/Test_Bank_Architecture.html)

## Project layout

```
src/main/api/
  tests/          # scenarios
  steps/          # AdminSteps, UserSteps
  foundation/     # requesters, endpoints, http_context
  db/             # models, crud, assertions
  fixtures/       # pytest fixtures
  specs/          # request/response/contract specs
```
