"""Heading element class."""
from typing import Optional
from playwright.sync_api import Page, expect
import allure
from .base_element import BaseElement


class Heading(BaseElement):
    """Represents a heading element (h1, h2, etc.)."""

    def __init__(self, page: Page, name: str, heading_text: Optional[str] = None) -> None:
        """
        Initialize a Heading element.
        
        Args:
            page: The Playwright Page object
            name: Human-readable name for the heading
            heading_text: Optional specific heading text to search for
        """
        text_to_find = heading_text or name
        element_locator = page.get_by_role('heading', name=text_to_find).first
        super().__init__(page, element_locator, name)
        self.heading_text = text_to_find

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'heading'

    @allure.step
    def get_text(self) -> str:
        """Get the text content of the heading."""
        with allure.step(f'Get text from {self.type_of} "{self.component_name}"'):
            self.element_locator.wait_for(state='visible')
            return self.element_locator.text_content() or ''

    @allure.step
    def should_have_text(self, expected_text: str) -> None:
        """Assert heading has expected text."""
        with allure.step(f'{self.type_of_upper} "{self.component_name}" should have text "{expected_text}"'):
            self.element_locator.wait_for(state='visible')
            expect(self.element_locator).to_contain_text(expected_text)