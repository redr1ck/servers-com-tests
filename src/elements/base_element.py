"""Base element class for UI components."""
from typing import Optional
from abc import ABC
from playwright.sync_api import Page, Locator, expect
import allure


class BaseElement(ABC):
    """Abstract base class for all UI elements in Playwright tests."""

    def __init__(
        self, 
        page: Page, 
        element_locator: Locator, 
        name: Optional[str] = None
    ):
        """
        Initialize a BaseElement.
        
        Args:
            page: The Playwright Page object
            element_locator: The Playwright Locator for the specific UI element
            name: An optional human-readable name for the element
        """
        self.page = page
        self.element_locator = element_locator
        self._name = name

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element (e.g., 'element')."""
        return 'element'

    @property
    def type_of_upper(self) -> str:
        """Gets the capitalized type of the element (e.g., 'Element', 'Button')."""
        return self.type_of.capitalize()

    @property
    def component_name(self) -> str:
        """Gets the human-readable name of the element."""
        if not self._name:
            raise ValueError('Provide "name" property to use "component_name"')
        return self._name

    def _get_error_message(self, action: str) -> str:
        """Generates a standardized error message for element actions."""
        return f'The {self.type_of} with name "{self.component_name}" and locator {self.element_locator} {action}'

    @allure.step
    def should_be_visible(self) -> None:
        """Asserts that the element is visible on the page."""
        with allure.step(f'{self.type_of_upper} "{self.component_name}" should be visible on the page'):
            self.element_locator.wait_for(state='visible')

    @allure.step
    def should_have_text(self, text: str) -> None:
        """Asserts that the element contains the specified text."""
        with allure.step(f'{self.type_of_upper} "{self.component_name}" should have text "{text}"'):
            self.element_locator.wait_for(state='visible')
            expect(self.element_locator).to_contain_text(text)

    @allure.step
    def should_contain_text(self, text: str) -> None:
        """Asserts that the element contains the specified text (alias for should_have_text)."""
        with allure.step(f'{self.type_of_upper} "{self.component_name}" should contain text "{text}"'):
            self.element_locator.wait_for(state='visible')
            expect(self.element_locator).to_contain_text(text)

    @allure.step
    def click(self) -> None:
        """Clicks on the element."""
        with allure.step(f'Clicking the {self.type_of} with name "{self.component_name}"'):
            self.element_locator.click()

    @allure.step
    def should_be_enabled(self) -> None:
        """Asserts that the element is enabled."""
        with allure.step(f'Checking if the {self.type_of} with name "{self.component_name}" is enabled'):
            self.element_locator.wait_for(state='enabled')

    @allure.step
    def wait_for_visible(self) -> None:
        """Waits for the element to become visible."""
        with allure.step(f'Waiting for the {self.type_of} with name "{self.component_name}" to be visible'):
            self.element_locator.wait_for(state='visible')