"""Identity and Access submenu class."""
import re
from playwright.sync_api import Page, Locator
from .submenu import SubMenu
from .menu_item import MenuItem
from .menu_item_config import MenuItemConfig


class IdentityAndAccessSubMenu(SubMenu):
    """Identity and Access submenu with specific items."""

    def __init__(self, page: Page, locator: Locator, config: MenuItemConfig):
        super().__init__(page, locator, config)

        self.ssh_gpg_keys = MenuItem(
            page,
            page.get_by_role('link', name=re.compile(r'SSH.*GPG.*keys', re.I)),
            MenuItemConfig('SSH & GPG keys', '/iam/keys', False)
        )

        self.api_tokens = MenuItem(
            page,
            page.get_by_role('link', name='API tokens').first,
            MenuItemConfig('API tokens', '/iam/api-tokens', False)
        )

