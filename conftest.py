"""
Root conftest.py for pytest configuration.
"""

import json
import random
from pathlib import Path
from io import StringIO

import pytest
import allure

from src.models.test_data import UserCredentials
from src.utils.logger import Logger


# Initialize logger
logger = Logger()


@pytest.fixture(scope="function", autouse=True)
def capture_logs_to_allure(request: pytest.FixtureRequest):
    """Capture logs for each test and attach to Allure report."""
    log_capture = StringIO()

    # Add a sink that captures to StringIO
    handler_id = logger._instance.add(
        log_capture,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="DEBUG",
    )

    yield

    # After test completes, attach logs to Allure
    logger._instance.remove(handler_id)
    log_content = log_capture.getvalue()

    if log_content:
        allure.attach(
            log_content,
            name=f"Test Logs: {request.node.name}",
            attachment_type=allure.attachment_type.TEXT,
        )


@pytest.fixture(scope="function")
def random_user() -> UserCredentials:
    """
    Get random user credentials from test data.

    Loads users from tests/test_data/users.json and returns a random one.

    Example:
        def test_login(random_user):
            login_page.login(random_user.email, random_user.password)
    """
    logger.info("Loading random user credentials from test data")
    test_data_path = Path(__file__).parent / "tests" / "test_data" / "users.json"

    with open(test_data_path, "r") as f:
        data = json.load(f)

    user = UserCredentials(**random.choice(data["users"]))
    logger.info(f"Selected user: {user.email}")
    return user
