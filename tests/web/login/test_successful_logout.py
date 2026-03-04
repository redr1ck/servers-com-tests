"""Successful logout test."""
import allure
from playwright.sync_api import Page, expect

from src.pages.login_page import LoginPage
from src.pages.platform.dashboard_page import DashboardPage


@allure.epic("Authentication")
@allure.feature("Logout")
@allure.story("Logout Process")
@allure.title("Successful Logout Flow")
@allure.description("Test successful logout process from dashboard to login page")
def test_successful_logout_flow(authorized_page: Page, page: Page) -> None:
    """Test successful logout from dashboard to login page."""
    page, _ = authorized_page
    dashboard_page = DashboardPage(page)
    dashboard_page.open()

    with allure.step("Verify user is logged in on dashboard"):
        dashboard_page.verify_user_is_logged_in()

    with allure.step("Open user profile dropdown and verify options"):
        dashboard_page.header.open_user_profile_dropdown()
        dashboard_page.header.verify_user_profile_dropdown_is_visible()

    with allure.step("Perform logout"):
        # Click logout button directly and wait for navigation to login page
        dashboard_page.header.logout_button.click()
        # Wait for redirect to login page
        page.wait_for_url("**/login", timeout=15000)
        page.wait_for_load_state("domcontentloaded")

    with allure.step("Verify logout completion"):
        # Verify we're on login page by checking URL
        expect(page).to_have_url("https://portal.servers.com/login")

        # Verify login page elements are visible
        login_page_after_logout = LoginPage(page)
        expect(login_page_after_logout.email_input).to_be_visible()
        expect(login_page_after_logout.password_input).to_be_visible()
        expect(login_page_after_logout.sign_in_button).to_be_visible()
        expect(login_page_after_logout.forgot_password_link).to_be_visible()
        expect(login_page_after_logout.join_link).to_be_visible()
