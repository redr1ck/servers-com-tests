from collections.abc import Generator
from typing import Any, Dict

import pytest
import allure
from playwright.sync_api import Page, Route, expect

from src.models.contac_form import ContactFormData
from src.pages.login_page import LoginPage
from src.models.test_data import UserCredentials
from src.utils.config_loader import get_test_config
from src.utils.generic import generate_contact_request_data
from src.utils.logger import Logger

logger = Logger()

_config = get_test_config()
BASE_URL: str = _config.web.base_url if _config.web else "https://portal.servers.com"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom pytest CLI options"""
    parser.addoption(
        "--proxy",
        action="store",
        default=None,
        help="Use proxy server. Provide address (e.g., 'socks5://127.0.0.1:9050'). "
             "Example: pytest --proxy='socks5://127.0.0.1:9050'",
    )

@pytest.fixture(autouse=True)
def global_playwright_timeouts(page: Page) -> None:
    """Set global timeouts for Playwright actions"""
    page.set_default_timeout(40_000)
    page.set_default_navigation_timeout(40_000)
    expect.set_options(timeout=20_000)

@pytest.fixture(scope="session")
def context_args(pytestconfig: pytest.Config) -> Dict[str, Any]:
    """Configure context options with optional proxy"""
    args: Dict[str, Any] = {
        "viewport": {"width": 1920, "height": 1080},
    }
    
    proxy_server = pytestconfig.getoption("--proxy")
    if proxy_server:
        args["proxy"] = {"server": proxy_server}
    
    return args

@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: Dict[str, Any],
    context_args: Dict[str, Any],
) -> Dict[str, Any]:
    """Merge custom context_args with Playwright's browser_context_args"""
    return {**browser_context_args, **context_args}


@pytest.fixture(autouse=True)
def block_cookiebot(page: Page) -> None:
    """Block CookieBot requests"""

    def _abort(route: Route) -> None:
        route.abort()

    page.route("**/consent.cookiebot.com/**", _abort)


@pytest.fixture(autouse=True)
def allure_browser_info(browser_name: str) -> None:
    allure.dynamic.parameter("browser", browser_name)
    allure.dynamic.tag(browser_name)
    allure.dynamic.parent_suite(browser_name.capitalize())

@pytest.fixture
def login_page(page: Page) -> Generator[LoginPage, None, None]:
    """Create login page instance with fresh state"""
    login_page = LoginPage(page)
    login_page.open()
    yield login_page

@pytest.fixture()
def authorized_page(page: Page, random_user: UserCredentials) -> Generator[Page, None, None]:
    """Log in with valid credentials and return the authorized page"""
    logger.info(f"Attempting login for user: {random_user.email}")
    user = random_user
    # Ensure we're on login page
    response = page.request.post(
        f"{BASE_URL}/auth/login",
        data={'email': user.email, 'password': user.password}
    )
    if response.status != 200:
        logger.error(f"Login API request failed with status {response.status}")
        raise Exception(f"Login API request failed with status {response.status}")

    logger.success(f"Successfully logged in as {user.email}")
    yield page
    logger.info("Authorized page fixture cleanup completed")


@pytest.fixture
def login_and_close_popups(authorized_page: Page) -> Page:
    """Log in and close any blocking popups (like NPS survey)"""
    from src.pages.platform.dashboard_page import DashboardPage
    dashboard = DashboardPage(authorized_page)
    dashboard.close_popups()
    return authorized_page

@pytest.fixture
def create_contact(page: Page) -> Generator[str, None, None]:
    """Fixture to create a contact before test."""
    logger.info("Creating contact via API")
    # Create a contact via API for testing
    contact_data = generate_contact_request_data()
    response = page.request.post(
        f"{BASE_URL}/rest/contacts",
        data=contact_data.model_dump_json(),
        headers={"Content-Type": "application/json"}
    )
    if response.status != 201:
        logger.error(f"Failed to create contact. Status: {response.status}, Response: {response.text}")
        raise Exception(f"Failed to create contact via API. Status: {response.status}, Response: {response.text}")

    contact_id = str(response.json()["data"]["id"])
    if not contact_id:
        logger.error("Contact creation response did not contain an ID")
        raise Exception("Contact creation response did not contain an ID.")

    logger.success(f"Contact created with ID: {contact_id}")
    yield contact_id
    logger.info(f"Contact {contact_id} fixture cleanup completed")


@pytest.fixture
def create_contact_and_cleanup(
    page: Page,
    cleanup_contacts: list[str],
) -> Generator[tuple[str, ContactFormData], None, None]:
    """Fixture to create a contact before test and ensure it's cleaned up after."""
    logger.info("Creating contact via API with cleanup")
    # Create a contact via API for testing
    contact_data = generate_contact_request_data()
    logger.debug(f"Contact data: {contact_data.model_dump_json()}")
    response = page.request.post(
        f"{BASE_URL}/rest/contacts",
        data=contact_data.model_dump_json(),
        headers={"Content-Type": "application/json"}
    )
    logger.debug(f"Response: {response.status}, {response.text}")
    if response.status != 201:
        logger.error(f"Failed to create contact. Status: {response.status}")
        raise Exception(f"Failed to create contact via API. Status: {response.status}, Response: {response.text}")
    
    contact_id = str(response.json()["data"]["id"])
    if not contact_id:
        logger.error("Contact creation response did not contain an ID")
        raise Exception("Contact creation response did not contain an ID.")
    coontact_form_data = ContactFormData(
        first_name=contact_data.fname,
        last_name=contact_data.lname,
        email=contact_data.email,
        secondary_email=contact_data.email2,
        phone=contact_data.phone_number,
        job_title=contact_data.tokens.title if contact_data.tokens else None,
        comment=contact_data.tokens.note if contact_data.tokens else None,
        is_primary=False,  # Assuming role 1 is primary
        is_emergency=True,  # Assuming role 2 is emergency
        is_billing=True,  # Assuming role 3 is billing
        is_technical=True,
        is_abuse=True  # Assuming role
    )
    
    # Add contact ID to cleanup list
    cleanup_contacts.append(contact_id)
    logger.success(f"Contact created with ID: {contact_id}, added to cleanup list")

    yield contact_id, coontact_form_data
    logger.info(f"Contact {contact_id} fixture cleanup - will be deleted by cleanup_contacts fixture")


@pytest.fixture
def cleanup_contacts(page: Page) -> Generator[list[str], None, None]:
    """
    Fixture to clean up contacts after test teardown.
    Usage: Append contact IDs to the list during test, they will be deleted after.

    Example:
        def test_something(cleanup_contacts):
            # Create contact, get ID
            contact_id = create_contact()
            cleanup_contacts.append(contact_id)
            # ... rest of test
            # cleanup happens automatically after test
    """
    contact_ids_to_delete = []
    logger.debug("Cleanup contacts fixture initialized")

    yield contact_ids_to_delete

    # Teardown: delete contacts after test completes
    if contact_ids_to_delete:
        logger.info(f"Cleaning up {len(contact_ids_to_delete)} contacts: {contact_ids_to_delete}")
        with allure.step(f"Cleanup: Delete {len(contact_ids_to_delete)} contacts"):
            for contact_id in contact_ids_to_delete:
                try:
                    logger.debug(f"Deleting contact {contact_id}")
                    response = page.request.delete(
                        f"{_config.web.base_url}/rest/contacts/{contact_id}"
                    )
                    logger.info(f"Contact {contact_id} deleted: status {response.status}")
                    allure.attach(
                        f"Contact {contact_id}: {response.status}",
                        name=f"Delete contact {contact_id}",
                        attachment_type=allure.attachment_type.TEXT
                    )
                except Exception as exc:
                    logger.error(f"Failed to delete contact {contact_id}: {str(exc)}")
                    allure.attach(
                        f"Failed to delete contact {contact_id}: {str(exc)}",
                        name=f"Delete contact {contact_id} - Error",
                        attachment_type=allure.attachment_type.TEXT
                    )
    else:
        logger.debug("No contacts to cleanup")
