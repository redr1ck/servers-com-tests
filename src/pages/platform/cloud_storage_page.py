"""Cloud Storage page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class CloudStoragePage(DashboardPage):
    """Cloud Storage Page Object Model.
    URL: /cloud-storage
    """

    def __init__(self, page: Page):
        """
        Initialize CloudStoragePage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/cloud-storage"
        self.page_heading = Heading(page, 'Cloud Storage')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Cloud Storage page is loaded."""
        with allure.step('Verify Cloud Storage page is loaded'):
            self.verify_url('/cloud-storage')
            self.page_heading.should_be_visible()
