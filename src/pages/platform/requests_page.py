"""Requests page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class RequestsPage(DashboardPage):
    """Requests Page Object Model.
    URL: /requests
    """

    def __init__(self, page: Page):
        """
        Initialize RequestsPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/requests"
        self.page_heading = Heading(page, 'Requests')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Requests page is loaded."""
        with allure.step('Verify Requests page is loaded'):
            self.verify_url('/requests')
            self.page_heading.should_be_visible()
