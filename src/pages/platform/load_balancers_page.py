"""Load Balancers page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class LoadBalancersPage(DashboardPage):
    """Load Balancers Page Object Model.
    URL: /lb
    """

    def __init__(self, page: Page):
        """
        Initialize LoadBalancersPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/lb"
        self.page_heading = Heading(page, 'Load Balancers')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Load Balancers page is loaded."""
        with allure.step('Verify Load Balancers page is loaded'):
            self.verify_url('/lb')
            self.page_heading.should_be_visible()
