# Test_Bank_org

Фреймворк API-автотестов для банковского backend: `pytest`, `Pydantic`, проверки PostgreSQL и Allure-логирование в requesters-слое.

## Требования

- Python 3.12+
- Запущенный Bank API (Swagger: `http://localhost:4111/api/swagger`)
- PostgreSQL со схемой backend (`dataBaseUrl` в конфиге)

## Быстрый старт

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Скопируйте `resources/urls.properties.example` в `resources/urls.properties` (или отредактируйте существующий файл).

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

## Тестовое покрытие

**40 тестов** (smoke — 8). Интеграционные тесты изменяют данные в общей БД, поэтому рекомендуется отдельная тестовая база.

Бизнес-лимиты (`deposit / transfer / credit`) находятся в `src/main/api/configs/business_limits.py`
и могут быть переопределены через `resources/urls.properties`.

## Покрытие API (Swagger ↔ framework)

| Swagger | Steps | Tests |
|---------|-------|-------|
| `POST /auth/token/login` | `AdminSteps.login_user` | `login_user_test` |
| `POST /admin/create` | `AdminSteps.create_user` | `create_user_test` |
| `GET /admin/users` | `AdminSteps.list_users` | `admin_list_users_test` (+ 401 без токена) |
| `DELETE /admin/users/{id}` | `AdminSteps.delete_user` | teardown в `object_fixture` |
| `POST /account/create` | `UserSteps.create_account` | `create_account_test` |
| `POST /account/deposit` | `UserSteps.deposit` | `deposit_account_test` |
| `POST /account/transfer` | `UserSteps.transfer` | `transfer_account_test` (между своими счетами) |
| `POST /credit/request` | `UserSteps.credit_request` | `credit_request_test` (+ проверки границ сумм) |
| `GET /credit/history` | `UserSteps.credit_history` | `credit_history_test` |
| `POST /credit/repay` | `UserSteps.credit_repay` | `credit_repay_test` |

## Документация

- [Test_Bank_Org_Onboarding.md](../Full%20description%20of%20the%20framework%20projects/Test_Bank_Org_Onboarding.md)
- [Test_Bank_Architecture.html](../Full%20description%20of%20the%20framework%20projects/Test_Bank_Architecture.html)

## Структура проекта

```
src/main/api/
  tests/          # тестовые сценарии
  steps/          # AdminSteps, UserSteps
  foundation/     # requesters, endpoints, http_context
  db/             # модели, crud, assertions
  fixtures/       # pytest-фикстуры
  specs/          # request/response/contract specs
```

## Сдача
Ветка сдачи: `Xataponx`.
