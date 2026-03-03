import pytest
from src.pages.login_page import LoginPage
from playwright.sync_api import Page



@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Create login page instance with fresh state"""
    login_page = LoginPage(page)
    login_page.open()
    return login_page
