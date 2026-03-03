"""Identity and Access page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class IdentityAndAccessPage(DashboardPage):
    """Identity and Access Page Object Model.
    URL: /iam
    """

    def __init__(self, page: Page):
        """
        Initialize IdentityAndAccessPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/iam"
        self.page_heading = Heading(page, 'Identity and Access')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Identity and Access page is loaded."""
        with allure.step('Verify Identity and Access page is loaded'):
            self.verify_url('/iam')
            self.page_heading.should_be_visible()
