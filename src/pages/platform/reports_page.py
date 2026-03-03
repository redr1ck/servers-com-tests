"""Reports page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class ReportsPage(DashboardPage):
    """Reports Page Object Model.
    URL: /reports
    """

    def __init__(self, page: Page):
        """
        Initialize ReportsPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/reports"
        self.page_heading = Heading(page, 'Reports')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Reports page is loaded."""
        with allure.step('Verify Reports page is loaded'):
            self.verify_url('/reports')
            self.page_heading.should_be_visible()
