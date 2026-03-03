"""Scalable Bare Metal page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class ScalableBareMetalPage(DashboardPage):
    """Scalable Bare Metal Page Object Model.
    URL: /sbm
    """

    def __init__(self, page: Page):
        """
        Initialize ScalableBareMetalPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/sbm"
        self.page_heading = Heading(page, 'Scalable Bare Metal')

    @allure.step
    def click_from_menu(self) -> None:
        """Click on Scalable Bare Metal from the side menu."""
        with allure.step('Click Scalable Bare Metal from menu'):
            self.side_menu.scalable_bare_metal.click()

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Scalable Bare Metal page is loaded."""
        with allure.step('Verify Scalable Bare Metal page is loaded'):
            self.verify_url('/sbm')
            self.page_heading.should_be_visible()
