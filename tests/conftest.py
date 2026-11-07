import pytest
from praktikum.burger import Burger
from unittest.mock import Mock


@pytest.fixture
def burger():
    return Burger()

@pytest.fixture
def bun():
    mock_bun = Mock()
    mock_bun.get_name.return_value = "krator bun"
    mock_bun.get_price.return_value = 50
    return mock_bun
