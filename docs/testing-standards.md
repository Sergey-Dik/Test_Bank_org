# Стандарты тестирования

## Слои

`tests -> fixtures -> ApiManager -> Steps -> Requesters -> build_api_url / Endpoint -> backend`

Параллельно для проверок БД: `db_session -> DbAssertions / CRUD -> PostgreSQL`.

## Изоляция данных

- Для новых пользователей используйте `with_unique_username(...)`
- Когда есть лимит суммы пополнения за одну операцию, используйте `fund_account(...)` (внутри `get_limits()` из `configs/business_limits.py`)
- Для обычных сумм вне границ используйте `generators/amount_generator.py`; границы — только `pytest.mark.parametrize`
- Фикстуры возвращают Pydantic-контексты (`UserAccountContext`, `CreditReadyContext` и т.д.), не tuple

## Бизнес-лимиты

- Значения по умолчанию: deposit 1000–9000, transfer 500–10000, credit 5000–15000
- Переопределение в `urls.properties`: `deposit.min`, `deposit.max` и т.д.

## Проверки в БД

- Модели синхронизированы с PostgreSQL: `user`, `account`, `credit`, `transaction`
- Для `transaction` используйте поля `transaction_type`, `to_account_id`, `from_account_id`
- Для проверок используйте `DbAssertions` / CRUD, а не сырой SQL

## Контракты

- Steps/requester выполняют HTTP и возвращают `Response`; проверки статуса и контракта — в тестах через `tests/api_assertions.py` (`assert_ok`, `assert_unauthorized`, …)
- Для разных форм ответа держите отдельные Pydantic-модели (например, `CreditRepayResponse`)

## CI-гейты

- `ruff check src conftest.py scripts`
- `pytest` и `pytest -n auto --dist=loadscope` — 42 теста
