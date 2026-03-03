"""Networks page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class NetworksPage(DashboardPage):
    """Networks Page Object Model.
    URL: /networks
    """

    def __init__(self, page: Page):
        """
        Initialize NetworksPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/networks"
        self.page_heading = Heading(page, 'Networks')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Networks page is loaded."""
        with allure.step('Verify Networks page is loaded'):
            self.verify_url('/networks')
            self.page_heading.should_be_visible()
