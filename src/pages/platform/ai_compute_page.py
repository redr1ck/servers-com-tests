"""AI Compute page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class AIComputePage(DashboardPage):
    """AI Compute Page Object Model.
    URL: /ai-compute
    """

    def __init__(self, page: Page):
        """
        Initialize AIComputePage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/ai-compute"
        self.page_heading = Heading(page, 'AI compute')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify AI Compute page is loaded."""
        with allure.step('Verify AI Compute page is loaded'):
            self.verify_url('/ai-compute')
            self.page_heading.should_be_visible()
