import allure
from abc import ABC, abstractmethod
import re
from playwright.sync_api import Page, Locator, expect

from src.utils.config_loader import get_test_config


_config = get_test_config()

class BasePage(ABC):
    def __init__(self, page: Page) -> None:
        self.page = page
        # Use config base_url if available, otherwise use default
        self.base_url = _config.web.base_url if _config.web else "https://portal.servers.com"

    @abstractmethod
    def open(self) -> None:
        """Navigate to the page URL. Must be implemented in subclass."""
        ...

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate(self, url: str) -> None:
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)

    def reload(self) -> None:
        with allure.step("Reload page"):
            self.page.reload()

    def go_back(self) -> None:
        with allure.step("Go back"):
            self.page.go_back()

    def get_current_url(self) -> str:
        with allure.step("Get current URL"):
            return self.page.url

    def get_title(self) -> str:
        with allure.step("Get page title"):
            return self.page.title()

    # ── Finders ───────────────────────────────────────────────────────────────

    def get_by_locator(self, locator: str) -> Locator:
        return self.page.locator(locator)

    def get_by_test_id(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(test_id)

    def get_by_text(self, text: str) -> Locator:
        return self.page.get_by_text(text)

    def get_by_role(self, role: str, name: str = "") -> Locator:
        return self.page.get_by_role(role, name=name)

    # ── Actions ───────────────────────────────────────────────────────────────

    def click(self, locator: str) -> None:
        with allure.step(f"Click on '{locator}'"):
            self.page.locator(locator).click()

    def double_click(self, locator: str) -> None:
        with allure.step(f"Double click on '{locator}'"):
            self.page.locator(locator).dblclick()

    def fill(self, locator: str, value: str) -> None:
        with allure.step(f"Fill '{locator}' with '{value}'"):
            self.page.locator(locator).fill(value)

    def clear(self, locator: str) -> None:
        with allure.step(f"Clear '{locator}'"):
            self.page.locator(locator).clear()

    def select_option(self, locator: str, value: str) -> None:
        with allure.step(f"Select option '{value}' in '{locator}'"):
            self.page.locator(locator).select_option(value)

    def check(self, locator: str) -> None:
        with allure.step(f"Check '{locator}'"):
            self.page.locator(locator).check()

    def uncheck(self, locator: str) -> None:
        with allure.step(f"Uncheck '{locator}'"):
            self.page.locator(locator).uncheck()

    def hover(self, locator: str) -> None:
        with allure.step(f"Hover over '{locator}'"):
            self.page.locator(locator).hover()

    def press_key(self, locator: str, key: str) -> None:
        with allure.step(f"Press key '{key}' on '{locator}'"):
            self.page.locator(locator).press(key)

    def upload_file(self, locator: str, path: str) -> None:
        with allure.step(f"Upload file '{path}' to '{locator}'"):
            self.page.locator(locator).set_input_files(path)

    # ── Waits ─────────────────────────────────────────────────────────────────

    def wait_for_visible(self, locator: str, timeout: int = 30_000) -> None:
        with allure.step(f"Wait for '{locator}' to be visible"):
            self.page.locator(locator).wait_for(state="visible", timeout=timeout)

    def wait_for_hidden(self, locator: str, timeout: int = 30_000) -> None:
        with allure.step(f"Wait for '{locator}' to be hidden"):
            self.page.locator(locator).wait_for(state="hidden", timeout=timeout)

    def wait_for_url(self, url: str, timeout: int = 30_000) -> None:
        with allure.step(f"Wait for URL to contain '{url}'"):
            self.page.wait_for_url(url, timeout=timeout)

    def wait_for_load_state(self, state: str = "networkidle") -> None:
        with allure.step(f"Wait for load state '{state}'"):
            self.page.wait_for_load_state(state)

    # ── Assertions ────────────────────────────────────────────────────────────

    def should_be_visible(self, locator: str) -> None:
        with allure.step(f"Assert '{locator}' is visible"):
            expect(self.page.locator(locator)).to_be_visible()

    def should_be_hidden(self, locator: str) -> None:
        with allure.step(f"Assert '{locator}' is hidden"):
            expect(self.page.locator(locator)).to_be_hidden()

    def should_have_text(self, locator: str, text: str) -> None:
        with allure.step(f"Assert '{locator}' has text '{text}'"):
            expect(self.page.locator(locator)).to_have_text(text)

    def should_have_value(self, locator: str, value: str) -> None:
        with allure.step(f"Assert '{locator}' has value '{value}'"):
            expect(self.page.locator(locator)).to_have_value(value)

    def should_be_enabled(self, locator: str) -> None:
        with allure.step(f"Assert '{locator}' is enabled"):
            expect(self.page.locator(locator)).to_be_enabled()

    def should_be_disabled(self, locator: str) -> None:
        with allure.step(f"Assert '{locator}' is disabled"):
            expect(self.page.locator(locator)).to_be_disabled()

    def should_be_checked(self, locator: str) -> None:
        with allure.step(f"Assert '{locator}' is checked"):
            expect(self.page.locator(locator)).to_be_checked()

    def should_have_url(self, url: str) -> None:
        with allure.step(f"Assert current URL is '{url}'"):
            expect(self.page).to_have_url(url)

    def should_have_title(self, title: str) -> None:
        with allure.step(f"Assert page title is '{title}'"):
            expect(self.page).to_have_title(title)

    # ── URL Verification ───────────────────────────────────────────────────────

    def verify_url(self, expected_path: str) -> None:
        with allure.step(f"Verify URL contains '{expected_path}'"):
            current_url = self.get_current_url()
            assert re.search(expected_path, current_url), (
                f"Expected URL to contain '{expected_path}', "
                f"but got '{current_url}'"
            )

    # ── Screenshots ───────────────────────────────────────────────────────────

    def take_screenshot(self, name: str = "screenshot") -> None:
        with allure.step(f"Take screenshot '{name}'"):
            screenshot = self.page.screenshot()
            allure.attach(
                screenshot,
                name=name,
                attachment_type=allure.attachment_type.PNG,
            )
