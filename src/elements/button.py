"""Button element class."""
from playwright.sync_api import Page
import allure
from .base_element import BaseElement
from typing import Optional


class Button(BaseElement):
    """Represents a button element."""

    def __init__(self, page: Page, name: str, selector: Optional[str] = None) -> None:
        """
        Initialize a Button element.
        
        Args:
            page: The Playwright Page object
            name: Human-readable name for the button
            selector: Optional CSS selector. If not provided, searches by role and name
        """
        if selector:
            element_locator = page.locator(selector).first
        else:
            element_locator = page.get_by_role("button", name=name).first

        super().__init__(page, element_locator, name)

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'button'

    @allure.step
    def click(self) -> None:
        """Click the button."""
        with allure.step(f'Click {self.type_of} "{self.component_name}"'):
            self.element_locator.wait_for(state='visible')
            self.element_locator.click()

    @allure.step
    def wait_for_enabled(self) -> None:
        """Wait for button to be enabled."""
        with allure.step(f'Wait for {self.type_of} "{self.component_name}" to be enabled'):
            # Note: Playwright's wait_for() only supports 'attached', 'detached', 'hidden', 'visible'
            # For enabled check, use is_enabled() or expect()
            from playwright.sync_api import expect
            self.element_locator.wait_for(state='visible')
            expect(self.element_locator).to_be_enabled()
