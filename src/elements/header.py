"""Header element class."""
from playwright.sync_api import Page
import allure
from .base_element import BaseElement


class Header(BaseElement):
    """Represents the main navigation header (<nav>) element."""

    def __init__(self, page: Page) -> None:
        """
        Initialize a Header element.
        
        Args:
            page: The Playwright Page object
        """
        element_locator = page.locator('nav').first
        super().__init__(page, element_locator, 'Header')

        self.logo = self.element_locator.locator('[alt*="logo"], [alt*="servers.com"]').first
        self.dashboard_link = self.element_locator.get_by_role('link', name='dashboard').first
        self.search_input = self.element_locator.locator('[role="searchbox"], input[placeholder*="Search"]').first
        self.user_menu = self.element_locator.locator('[class*="user"], [data-testid="user-menu"]').first

        # User profile dropdown elements - using structural selectors
        self.user_profile_button = self.page.locator('header button, [role="banner"] button, nav button').last
        self.user_profile_link = self.page.get_by_role('link').filter(has_text='@').first
        self.logout_button = self.page.get_by_role('button', name='Logout')
        self.create_account_link = self.page.get_by_role('link', name='Create new account')

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'header'

    @allure.step
    def click_dashboard(self) -> None:
        """Click on the dashboard link in the header."""
        with allure.step('Click Dashboard link in header'):
            self.dashboard_link.click()
            self.page.wait_for_load_state('load')

    @allure.step
    def should_be_visible(self) -> None:
        """Verify header is visible on the page."""
        with allure.step('Verify Header is visible'):
            self.element_locator.wait_for(state='visible')

    @allure.step("Open user profile dropdown")
    def open_user_profile_dropdown(self) -> None:
        """Click on user profile button to open dropdown."""
        with allure.step('Open user profile dropdown'):
            self.user_profile_button.wait_for(state='visible')
            self.user_profile_button.click()
            # Wait for dropdown menu to render
            self.page.wait_for_timeout(500)

    @allure.step("Verify user profile dropdown elements")
    def verify_user_profile_dropdown_is_visible(self) -> None:
        """Verify user profile dropdown is visible with all expected elements."""
        from playwright.sync_api import expect
        with allure.step('Verify user profile dropdown elements'):
            expect(self.user_profile_link).to_be_visible()
            expect(self.logout_button).to_be_visible()
            expect(self.create_account_link).to_be_visible()

    @allure.step("Click logout button")
    def click_logout(self) -> None:
        """Perform logout action by clicking logout button."""
        with allure.step('Click logout button'):
            self.logout_button.wait_for(state='visible', timeout=10000)
            self.logout_button.click()
            # Don't wait for networkidle - page is redirecting/closing
            self.page.wait_for_timeout(500)
