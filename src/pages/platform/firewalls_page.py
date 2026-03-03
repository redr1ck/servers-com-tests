"""Firewalls page object model."""
from playwright.sync_api import Page, Locator
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, Button, MENU_ITEMS


class FirewallsPage(DashboardPage):
    """Firewalls Page Object Model.
    URL: /firewalls
    """

    def __init__(self, page: Page):
        """
        Initialize FirewallsPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/fw"
        self.page_heading = Heading(page, 'Firewalls')
        self.create_button = Button(page, 'Create')  
        self.fw_content = page.locator('text=/firewall|security|rule|traffic/i').first

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Firewalls page is loaded."""
        with allure.step('Verify Firewalls page is loaded'):
            self.verify_url('/firewalls')
            self.page_heading.should_be_visible()
            self.create_button.should_be_visible()
            self.fw_content.wait_for(state='visible', timeout=10000)