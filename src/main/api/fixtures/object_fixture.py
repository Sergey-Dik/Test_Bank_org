import logging
from typing import Any

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.fixture
def created_obj():
    objects: list[Any] = []
    yield objects
    _cleanup(objects)


def _cleanup(objects: list[Any]) -> None:
    api_manager = ApiManager(objects)
    for item in objects:
        if isinstance(item, CreateUserResponse):
            try:
                api_manager.admin_steps.delete_user(item.id)
            except Exception as exc:
                logging.warning("Failed to delete user %s: %s", item.id, exc)
