"""Monitoring page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class MonitoringPage(DashboardPage):
    """Monitoring Page Object Model.
    URL: /monitoring
    """

    def __init__(self, page: Page):
        """
        Initialize MonitoringPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/monitoring"
        self.page_heading = Heading(page, 'Monitoring')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Monitoring page is loaded."""
        with allure.step('Verify Monitoring page is loaded'):
            self.verify_url('/monitoring')
            self.page_heading.should_be_visible()
