"""
Root conftest.py for pytest configuration.
"""

import json
import random
from pathlib import Path

import pytest

from src.models.test_data import UserCredentials


@pytest.fixture(scope="function")
def random_user() -> UserCredentials:
    """
    Get random user credentials from test data.

    Loads users from tests/test_data/users.json and returns a random one.

    Example:
        def test_login(random_user):
            login_page.login(random_user.email, random_user.password)
    """
    test_data_path = Path(__file__).parent / "tests" / "test_data" / "users.json"

    with open(test_data_path, "r") as f:
        data = json.load(f)

    return UserCredentials(**random.choice(data["users"]))
