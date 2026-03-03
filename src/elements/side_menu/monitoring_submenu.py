"""Monitoring submenu class."""
import re
from playwright.sync_api import Page, Locator
from .submenu import SubMenu
from .menu_item import MenuItem
from .menu_item_config import MenuItemConfig


class MonitoringSubMenu(SubMenu):
    """Monitoring submenu with specific items."""

    def __init__(self, page: Page, locator: Locator, config: MenuItemConfig):
        super().__init__(page, locator, config)

        self.healthchecks = MenuItem(
            page,
            page.get_by_role('link', name='Healthchecks').first,
            MenuItemConfig('Healthchecks', '/monitoring/healthchecks', False)
        )

        self.notifications = MenuItem(
            page,
            page.get_by_role('link', name='Notifications').first,
            MenuItemConfig('Notifications', '/monitoring/notifications', False)
        )

