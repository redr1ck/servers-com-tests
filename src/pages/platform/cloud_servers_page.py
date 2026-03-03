"""Cloud Servers page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class CloudServersPage(DashboardPage):
    """Cloud Servers Page Object Model.
    This menu item only expands submenu, doesn't navigate to a page.
    """

    def __init__(self, page: Page):
        """
        Initialize CloudServersPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/cloud-servers"
        self.page_heading = Heading(page, 'Cloud Servers')

    @allure.step
    def expand_submenu_only(self) -> None:
        """Expand the submenu."""
        with allure.step('Expand Cloud Servers submenu'):
            self.side_menu.expand_submenu_by_key('cloud_servers')

    @allure.step
    def verify_submenu_expanded(self) -> None:
        """Verify submenu is expanded (visible)."""
        with allure.step('Verify Cloud Servers submenu is expanded'):
            is_expanded = self.side_menu.is_submenu_expanded_by_key('cloud_servers')
            if not is_expanded:
                raise AssertionError('Cloud Servers submenu is not expanded')