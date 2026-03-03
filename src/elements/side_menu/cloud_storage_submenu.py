"""Cloud Servers submenu class."""
import re
from playwright.sync_api import Page, Locator
from .submenu import SubMenu
from .menu_item import MenuItem
from .menu_item_config import MenuItemConfig


class CloudStorageSubMenu(SubMenu):
    """Cloud Servers submenu with specific items."""

    def __init__(self, page: Page, locator: Locator, config: MenuItemConfig):
        super().__init__(page, locator, config)

        # Add specific menu items for Cloud Servers submenu
        self.servers = MenuItem(
            page,
            page.get_by_role('link', name='Cloud Storage').first,
            MenuItemConfig('Servers', '/cloud-storages', False)
        )

