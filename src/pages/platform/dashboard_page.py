"""Dashboard page base class."""
from typing import Optional
import re
from playwright.sync_api import Page, expect
import allure

from ..base_page import BasePage
from src.elements import Header, SideMenu


class DashboardPage(BasePage):
    """Base class for dashboard pages.
    """

    def __init__(self, page: Page):
        """
        Initialize a DashboardPage.
        
        Args:
            page: The Playwright Page object
            user_id: The user ID for session-aware URLs
        """
        super().__init__(page)
        self.header = Header(self.page)
        self.side_menu = SideMenu(self.page)
        self.url_path = "/dashboard"

        # Dashboard elements
        self.dashboard_text = self.page.get_by_text('dashboard')
        self.current_balance_text = self.page.get_by_text('Current balance')

    def get_session_prefix(self) -> Optional[str]:
        """Get session prefix from current URL."""
        current_url = self.page.url
        match = re.search(r'(\/a:[^\/]+)\/', current_url)
        return match.group(1) if match else None

    @allure.step
    def open(self) -> None:
        """Navigate to this page using session-aware URL."""
        with allure.step(f'Navigate to {self.url_path}'):
            session_prefix = self.get_session_prefix()
            if session_prefix:
                full_url = f'{self.base_url}{session_prefix}{self.url_path}'
            else:
                full_url = f'{self.base_url}{self.url_path}'
            
            self.page.goto(full_url)
            self.wait_for_load_state()
            self.url = self.page.url

    @allure.step("Wait for dashboard to load")
    def wait_for_dashboard_load(self) -> None:
        """Wait for dashboard to be fully loaded."""
        with allure.step('Wait for dashboard to load'):
            self.dashboard_text.wait_for(state='visible', timeout=30000)

    @allure.step("Verify user is logged in on dashboard")
    def verify_user_is_logged_in(self) -> None:
        """Verify that user is logged in and on dashboard."""
        with allure.step('Verify user is logged in on dashboard'):
            expect(self.dashboard_text).to_be_visible()
            expect(self.header.user_profile_button).to_be_visible()
            expect(self.current_balance_text).to_be_visible()

    @allure.step("Perform logout")
    def logout(self) -> None:
        """Complete logout flow - opens dropdown and clicks logout."""
        with allure.step('Complete logout flow'):
            self.header.open_user_profile_dropdown()
            self.header.click_logout()

    @allure.step
    def close_popups(self) -> None:
        """Close any blocking popups (like NPS survey)."""
        with allure.step('Close any blocking popups'):
            # Try to close NPS popup
            try:
                ok_button = self.page.get_by_role('button', name='OK').first
                ok_button.wait_for(state='visible', timeout=2000)
                ok_button.click()
                self.page.wait_for_timeout(500)
            except:
                pass  # No popup found, continue

    @allure.step
    def verify_url(self, url_pattern: str) -> None:
        """Verify page URL matches pattern."""
        with allure.step('Verify page URL'):
            current_url = self.page.url
            pattern = re.compile(url_pattern)
            if not pattern.search(current_url):
                raise AssertionError(f'URL {current_url} does not match pattern {url_pattern}')

    @allure.step
    def verify_header_visible(self) -> None:
        """Verify header is visible on the page."""
        with allure.step('Verify Header is visible'):
            self.header.should_be_visible()

    @allure.step
    def verify_side_menu_visible(self) -> None:
        """Verify side menu is visible on the page."""
        with allure.step('Verify Side Menu is visible'):
            self.side_menu.should_be_visible()