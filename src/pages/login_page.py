import re
import allure
from playwright.sync_api import Page, Locator, expect
from src.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Login Page Object Model
    URL: https://portal.servers.com/login
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url += "/login"

        # Inputs and buttons
        self.email_input: Locator = self.page.get_by_label("Email").nth(0)
        self.password_input: Locator = self.page.get_by_label("Password").nth(0)
        self.sign_in_button: Locator = self.page.get_by_role("button", name="Sign in")

        # Links
        self.forgot_password_link: Locator = self.page.get_by_role("link", name="Forgot your password?")
        self.join_link: Locator = self.page.get_by_role("link", name="or Join")

        # Error elements
        self.error_message: Locator = self.page.get_by_role("alert").or_(
            self.page.locator(".error-message, .alert-error")
        )
        self.validation_message: Locator = self.page.locator(".validation-message, .field-error, .error-text")

        # Attention icon and tooltip
        self.attention_icon: Locator = self.page.locator('svg[id="Icon/Attention"], [id="Icon/Attention"]')
        self.tooltip: Locator = self.page.locator('[role="tooltip"], .tooltip, .error-tooltip, [data-testid="error-tooltip"]')

    def open(self) -> None:
        with allure.step("Open Login Page"):
            self.page.goto(self.base_url)
        self.wait_for_load()

    def wait_for_load(self) -> None:
        """Wait for page to be loaded"""
        with allure.step("Wait for page load"):
            self.wait_for_load_state("networkidle")

    def enter_email(self, email: str) -> None:
        """Enter email in the email field"""
        with allure.step(f"Enter email: {email}"):
            self.email_input.wait_for(state="visible")
            self.email_input.fill(email)

    def enter_password(self, password: str) -> None:
        """Enter password in the password field"""
        with allure.step("Enter password"):
            self.password_input.wait_for(state="visible")
            self.password_input.fill(password)

    def click_sign_in(self) -> None:
        """Click Sign In button"""
        with allure.step("Click Sign In button"):
            self.sign_in_button.wait_for(state="visible")
            self.sign_in_button.click()

    def login(self, email: str, password: str) -> None:
        """Perform complete login with valid credentials"""
        with allure.step(f"Login with email: {email}"):
            self.enter_email(email)
            self.enter_password(password)
            self.click_sign_in()

    def click_forgot_password(self) -> None:
        """Click Forgot Password link"""
        with allure.step("Click Forgot Password link"):
            self.forgot_password_link.wait_for(state="visible")
            self.forgot_password_link.click()

    def click_join(self) -> None:
        """Click Join/Registration link"""
        with allure.step("Click Join link"):
            self.join_link.wait_for(state="visible")
            self.join_link.click()

    def verify_email_value(self, expected_email: str) -> None:
        """Verify email input contains expected value"""
        with allure.step(f"Verify email value: {expected_email}"):
            expect(self.email_input).to_have_value(expected_email)

    def verify_password_value(self, expected_password: str) -> None:
        """Verify password input contains expected value"""
        with allure.step("Verify password value"):
            expect(self.password_input).to_have_value(expected_password)

    def verify_error_message_visible(self) -> None:
        """Verify error message is visible"""
        with allure.step("Verify error message is visible"):
            self.error_message.wait_for(state="visible", timeout=10000)
            expect(self.error_message).to_be_visible()

    def verify_validation_message_visible(self) -> None:
        """Verify validation message is visible (HTML5 validation or custom)"""
        with allure.step("Verify validation message is visible"):
            is_email_invalid = self.email_input.evaluate(
                lambda el: not el.is_valid
            ) if self.email_input.evaluate("el => el.validity") else False

            is_password_invalid = self.password_input.evaluate(
                lambda el: not el.is_valid
            ) if self.password_input.evaluate("el => el.validity") else False

            if is_email_invalid or is_password_invalid:
                return

            self.validation_message.wait_for(state="visible", timeout=5000)
            expect(self.validation_message).to_be_visible()

    def verify_field_invalid(self, field: str) -> None:
        """Verify field has HTML5 validation error"""
        with allure.step(f"Verify {field} field is invalid"):
            input_locator = self.email_input if field == "email" else self.password_input
            is_invalid = input_locator.evaluate("el => !el.validity.valid")
            assert is_invalid, f"{field} field should be invalid"

    def verify_submission_blocked(self) -> None:
        """Verify form stayed on login page (submission was blocked)"""
        with allure.step("Verify submission was blocked"):
            expect(self.page).to_have_url(self.base_url)
            self.email_input.wait_for(state="visible")
            self.password_input.wait_for(state="visible")
            self.sign_in_button.wait_for(state="visible")

    def verify_error_message_text(self, expected_text: str) -> None:
        """Verify error message contains expected text"""
        with allure.step(f"Verify error message text: {expected_text}"):
            self.error_message.wait_for(state="visible", timeout=10000)
            expect(self.error_message).to_contain_text(expected_text)

    def verify_successful_login(self) -> None:
        """Verify successful login (redirect or success message)"""
        with allure.step("Verify successful login"):
            self.page.wait_for_url(re.compile(r"https://portal\.servers\.com/(?!login).*"), timeout=10000)

    def verify_url_contains(self, expected_path: str) -> None:
        """Verify current URL contains expected path"""
        with allure.step(f"Verify URL contains: {expected_path}"):
            self.page.wait_for_url(re.compile(re.escape(expected_path)), timeout=10000)

    def verify_title_contains(self, expected_text: str) -> None:
        """Verify page title contains expected text"""
        with allure.step(f"Verify title contains: {expected_text}"):
            expect(self.page).to_have_title(expected_text)

    def hover_attention_icon(self, field: str = "email") -> None:
        """Hover over attention icon for specified field"""
        with allure.step(f"Hover over attention icon for {field}"):
            icon = self.attention_icon.filter(has=self.page.locator(f"{field}_input ~ *")).first if field == "email" else self.attention_icon.last
            icon.wait_for(state="visible", timeout=5000)
            icon.hover()

    def verify_tooltip_visible(self) -> None:
        """Verify tooltip is visible"""
        with allure.step("Verify tooltip is visible"):
            self.tooltip.first.wait_for(state="visible", timeout=5000)
            expect(self.tooltip.first).to_be_visible()

    def verify_tooltip_text(self, expected_text: str) -> None:
        """Verify tooltip contains expected text"""
        with allure.step(f"Verify tooltip text: {expected_text}"):
            self.tooltip.first.wait_for(state="visible", timeout=5000)
            expect(self.tooltip.first).to_contain_text(expected_text)

    def verify_field_error_tooltip(self, field: str, expected_text: str) -> None:
        """
        Verify error tooltip for specific field.
        First checks HTML5 validationMessage, then tries to find visible tooltip.
        """
        with allure.step(f"Verify {field} field error tooltip"):
            # First, check HTML5 validation message (native browser validation)
            field_locator = self.email_input if field == "email" else self.password_input
            html5_message = field_locator.evaluate("el => el.validationMessage")
            
            if html5_message and expected_text in html5_message:
                allure.attach(
                    f"HTML5 validation message: {html5_message}",
                    name="HTML5 Validation Message",
                    attachment_type=allure.attachment_type.TEXT
                )
                return
            
            # Wait a bit for any custom tooltips to appear
            self.page.wait_for_timeout(1000)

            # Check if attention icon exists
            all_icons = self.page.locator('[id="Icon/Attention"]')
            if all_icons.count() > 0:
                all_icons.first.wait_for(state="visible", timeout=10000)
                all_icons.first.hover(force=True)
                self.page.wait_for_timeout(500)

            # Try to find tooltip with expected text
            tooltip = self.page.locator(f'text={expected_text}').first

            # If not found, try to find any visible tooltip and log its content
            if not tooltip.is_visible():
                # Look for common tooltip selectors
                possible_tooltips = self.page.locator('[role="tooltip"], .tooltip, .error-tooltip, [data-testid="error-tooltip"]')
                if possible_tooltips.count() > 0:
                    actual_text = possible_tooltips.first.text_content()
                    allure.attach(
                        f"Expected: {expected_text}\nActual tooltip text: {actual_text}",
                        name="Tooltip text comparison",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    # Check if expected text is contained in actual text (partial match)
                    if expected_text in actual_text:
                        return

            # Final attempt - wait for the tooltip
            tooltip.wait_for(state="visible", timeout=5000)
