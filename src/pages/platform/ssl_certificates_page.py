"""SSL Certificates page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class SSLCertificatesPage(DashboardPage):
    """SSL Certificates Page Object Model.
    URL: /ssl
    """

    def __init__(self, page: Page):
        """
        Initialize SSLCertificatesPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/ssl"
        self.page_heading = Heading(page, 'SSL certificates')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify SSL Certificates page is loaded."""
        with allure.step('Verify SSL Certificates page is loaded'):
            self.verify_url('/ssl')
            self.page_heading.should_be_visible()
