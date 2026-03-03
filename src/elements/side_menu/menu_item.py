"""Menu item element class."""
from playwright.sync_api import Page, Locator
import allure
from ..base_element import BaseElement
from .menu_item_config import MenuItemConfig


class MenuItem(BaseElement):
    """Represents a single menu item."""

    def __init__(self, page: Page, locator: Locator, config: MenuItemConfig):
        super().__init__(page, locator, config.name)
        self.config = config

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'menu item'

    @allure.step
    def click(self) -> None:
        """Click on this menu item."""
        with allure.step(f'Click on "{self.config.name}"'):
            self.element_locator.wait_for(state='visible', timeout=10000)
            self.element_locator.click()
            self.page.wait_for_load_state('load')
            self.page.wait_for_timeout(2000)

    @allure.step
    def should_be_visible(self) -> None:
        """Verify menu item is visible."""
        with allure.step(f'Verify "{self.config.name}" is visible'):
            self.element_locator.wait_for(state='visible', timeout=5000)

    @allure.step
    def should_not_be_visible(self) -> None:
        """Verify menu item is not visible."""
        with allure.step(f'Verify "{self.config.name}" is not visible'):
            self.element_locator.wait_for(state='hidden', timeout=5000)

