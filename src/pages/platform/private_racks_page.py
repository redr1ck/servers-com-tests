"""Private Racks page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class PrivateRacksPage(DashboardPage):
    """Private Racks Page Object Model.
    URL: /private-racks
    """

    def __init__(self, page: Page):
        """
        Initialize PrivateRacksPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/racks"
        self.page_heading = Heading(page, 'Private Racks')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Private Racks page is loaded."""
        with allure.step('Verify Private Racks page is loaded'):
            self.verify_url('/private-racks')
            self.page_heading.should_be_visible()
