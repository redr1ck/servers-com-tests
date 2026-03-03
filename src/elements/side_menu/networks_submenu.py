"""Networks submenu class."""
import re
from playwright.sync_api import Page, Locator
from .submenu import SubMenu
from .menu_item import MenuItem
from .menu_item_config import MenuItemConfig


class NetworksSubMenu(SubMenu):
    """Networks submenu with specific items."""

    def __init__(self, page: Page, locator: Locator, config: MenuItemConfig):
        super().__init__(page, locator, config)

        # Add specific menu items for Networks submenu
        self.private_networks = MenuItem(
            page,
            page.get_by_role('link', name=re.compile(r'Private.*[Nn]etworks', re.I)).first,
            MenuItemConfig('Private Networks', '/networks/private', False)
        )

