import pytest

from src.main.api.foundation.http_context import get_http_context


@pytest.fixture
def http_context():
    return get_http_context()
