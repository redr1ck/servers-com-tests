import pytest
import allure
from src.pages.login_page import LoginPage
from tests.web.conftest import login_page


@allure.feature("Login")
@allure.story("Field Validation")
class TestFieldValidation:
    """Tests for email and password field validation with tooltips"""

    @allure.title("Валидация поля Email")
    @pytest.mark.parametrize(
        "email,description,expected_error",
        [
            ("userexample.com", "Email without @ symbol", "Invalid email address"),
            ("user@@example.com", "Email with multiple @ symbols", "Invalid email address"),
            ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@example.com", "Email longer than 69 characters", "Invalid email address"),
        ],
        ids=["no_at_symbol", "multiple_at", "too_long"]
    )
    def test_email_validation(
        self,
        login_page: LoginPage,
        email: str,
        description: str,
        expected_error: str,
    ) -> None:
        """1.6 Email field validation with various invalid formats"""
        # Reload to ensure clean state for each parameter
        # login_page = LoginPage(page)
        # login_page.reload()
        # login_page.wait_for_load_state("networkidle")
        # login_page.open()
        # login_page.wait_for_load_state("networkidle")

        with allure.step(f"Enter {description}: {email[:30]}..."):
            # Fill email with invalid value
            login_page.enter_email(email)
            # Fill password with valid value to avoid password error tooltip
            login_page.enter_password("ValidPassword123!")
            login_page.verify_email_value(email)

            # Submit form
            login_page.click_sign_in()

            # Verify error tooltip appears with expected message
            login_page.verify_field_error_tooltip("email", expected_error)

    @allure.title("Валидация поля Password")
    @pytest.mark.parametrize(
        "password,description,expected_error",
        [
            ("short", "Password less than 10 characters", "Please enter at least 10 characters."),
            ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "Password longer than 64 characters", "Maximum allowed length is 64 characters"),
        ],
        ids=["too_short", "too_long"]
    )
    def test_password_validation(
        self,
        login_page: LoginPage,
        password: str,
        description: str,
        expected_error: str,
    ) -> None:
        """1.7 Password field validation"""
        # Reload to ensure clean state for each parameter
        # page.reload()
        # page.wait_for_load_state("networkidle")
        # page.goto("https://portal.servers.com/login")
        # page.wait_for_load_state("networkidle")

        with allure.step(f"Enter {description}"):
            # Fill password with invalid value
            login_page.enter_password(password)
            # Fill email with valid value to avoid email error tooltip
            login_page.enter_email("valid@example.com")
            login_page.verify_password_value(password)

            # Submit form
            login_page.click_sign_in()

            # Verify error tooltip appears with expected message
            login_page.verify_field_error_tooltip("password", expected_error)

    @allure.title("Валидация email 'n@l.' - точка в неправильной позиции")
    def test_email_validation_dot_at_wrong_position(
        self,
        login_page: LoginPage,
    ) -> None:
        """Email validation: '.' is used at a wrong position"""
        invalid_email = "n@l."

        with allure.step(f"Enter invalid email: {invalid_email}"):
            login_page.enter_email(invalid_email)
            login_page.verify_email_value(invalid_email)

        with allure.step("Submit form"):
            login_page.click_sign_in()

        with allure.step("Verify error tooltip for email field"):
            login_page.verify_field_error_tooltip("email", "'.' is used at a wrong position in 'l.'.")
