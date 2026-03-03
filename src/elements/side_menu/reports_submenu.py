"""Reports submenu class."""
import re
from playwright.sync_api import Page, Locator
from .submenu import SubMenu
from .menu_item import MenuItem
from .menu_item_config import MenuItemConfig


class ReportsSubMenu(SubMenu):
    """Reports submenu with specific items."""

    def __init__(self, page: Page, locator: Locator, config: MenuItemConfig):
        super().__init__(page, locator, config)

        # Add specific menu items for Reports submenu
        self.usage_reports = MenuItem(
            page,
            page.get_by_role('link', name=re.compile(r'Usage.*[Rr]eports', re.I)).first,
            MenuItemConfig('Usage Reports', '/reports/usage', False)
        )

