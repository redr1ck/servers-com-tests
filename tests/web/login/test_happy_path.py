import allure

from src.models.test_data import UserCredentials
from src.pages.login_page import LoginPage


@allure.feature("Login")
@allure.story("Happy Path")
class TestLoginHappyPath:
    """Tests for successful login scenarios"""

    @allure.title("Успешный вход с валидными данными")
    def test_successful_login(self, login_page: LoginPage, random_user: UserCredentials) -> None:
        """1.1 Successful login with valid credentials"""
        valid_email = random_user.email
        valid_password = random_user.password

        with allure.step("Enter valid email"):
            login_page.enter_email(valid_email)
            login_page.verify_email_value(valid_email)

        with allure.step("Enter valid password"):
            login_page.enter_password(valid_password)
            login_page.verify_password_value(valid_password)

        with allure.step("Click Sign In button"):
            login_page.click_sign_in()
            login_page.verify_successful_login()

    @allure.title("Ошибка при неверном пароле или email")
    def test_invalid_credentials_error(self, login_page: LoginPage) -> None:
        """1.2 Error message with invalid credentials"""
        invalid_email = "nonexistent@example.com"
        invalid_password = "WrongPassword123!"

        with allure.step("Enter non-existent email or wrong password"):
            login_page.enter_email(invalid_email)
            login_page.verify_email_value(invalid_email)
            login_page.enter_password(invalid_password)
            login_page.verify_password_value(invalid_password)

        with allure.step("Click Sign In button"):
            login_page.click_sign_in()
            login_page.verify_error_message_visible()

    @allure.title("Валидация пустых полей")
    def test_empty_fields_validation(self, login_page: LoginPage) -> None:
        """1.3 Empty fields validation"""
        with allure.step("Leave both fields empty and click Sign In"):
            login_page.click_sign_in()
            login_page.verify_submission_blocked()

        with allure.step("Fill only email and click Sign In"):
            login_page.enter_email("test@example.com")
            login_page.click_sign_in()
            login_page.verify_submission_blocked()

        with allure.step("Fill only password and click Sign In"):
            login_page.enter_password("Password123!")
            login_page.click_sign_in()
            login_page.verify_submission_blocked()

    @allure.title("Переход на восстановление пароля")
    def test_forgot_password_link(self, login_page: LoginPage) -> None:
        """1.4 Navigate to password recovery"""
        with allure.step("Click Forgot Password link"):
            login_page.click_forgot_password()
            login_page.verify_url_contains("/password/forgot")

    @allure.title("Переход на регистрацию")
    def test_registration_link(self, login_page: LoginPage) -> None:
        """1.5 Navigate to registration"""
        with allure.step("Click Join link"):
            login_page.click_join()
            login_page.verify_url_contains("/registration")
