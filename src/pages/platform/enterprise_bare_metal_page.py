"""Enterprise Bare Metal page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class EnterpriseBareMetalPage(DashboardPage):
    """Enterprise Bare Metal Page Object Model.
    URL: /enterprise
    """

    def __init__(self, page: Page):
        """
        Initialize EnterpriseBareMetalPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/ebm"
        self.page_heading = Heading(page, 'Enterprise Bare Metal')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Enterprise Bare Metal page is loaded."""
        with allure.step('Verify Enterprise Bare Metal page is loaded'):
            self.verify_url('/enterprise')
            self.page_heading.should_be_visible()
