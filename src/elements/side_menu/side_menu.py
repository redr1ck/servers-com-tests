"""Side menu element class."""
import re
from typing import List
from playwright.sync_api import Page, Locator
import allure

from .cloud_storage_submenu import CloudStorageSubMenu
from ..base_element import BaseElement
from .menu_item import MenuItem
from .submenu import SubMenu
from .menu_item_config import MenuItemConfig, MENU_ITEMS
from .monitoring_submenu import MonitoringSubMenu
from .identity_and_access_submenu import IdentityAndAccessSubMenu
from .billing_submenu import BillingSubMenu
from .enterprise_bare_metal_submenu import EnterpriseBareMetalSubMenu
from .cloud_servers_submenu import CloudServersSubMenu
from .networks_submenu import NetworksSubMenu
from .reports_submenu import ReportsSubMenu


class SideMenu(BaseElement):
    """Represents the side navigation menu element."""

    def __init__(self, page: Page):
        """
        Initialize a SideMenu element.

        Args:
            page: The Playwright Page object
        """
        element_locator = page.locator('body').first
        super().__init__(page, element_locator, 'Side Menu')

        # Find the main menu ul - try multiple possible selectors
        self.menu_list = self.page.locator('ul').first
        self.menu_items = self.menu_list.locator('> li')

        # Initialize direct navigation menu items
        self.scalable_bare_metal = MenuItem(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Scalable Bare Metal', re.I)).first,
            MENU_ITEMS['scalable_bare_metal']
        )

        self.ai_compute = MenuItem(
            self.page,
            self.menu_list.get_by_text(re.compile(r'AI compute', re.I)).first,
            MENU_ITEMS['ai_compute']
        )

        self.cloud_storage = MenuItem(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Cloud Storage', re.I)).first,
            MENU_ITEMS['cloud_storage']
        )

        self.managed_kubernetes = MenuItem(
            self.page,
            self.menu_list.get_by_text('Managed Kubernetes').first,
            MENU_ITEMS['managed_kubernetes']
        )

        self.load_balancers = MenuItem(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Load Balancers', re.I)).first,
            MENU_ITEMS['load_balancers']
        )

        self.firewalls = MenuItem(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Firewalls', re.I)).first,
            MENU_ITEMS['firewalls']
        )

        self.private_racks = MenuItem(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Private Racks', re.I)).first,
            MENU_ITEMS['private_racks']
        )

        self.ssl_certificates = MenuItem(
            self.page,
            self.menu_list.get_by_text(re.compile(r'SSL certificates', re.I)).first,
            MENU_ITEMS['ssl_certificates']
        )

        self.account_settings = MenuItem(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Account settings', re.I)).first,
            MENU_ITEMS['account_settings']
        )

        self.requests = MenuItem(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Requests', re.I)).first,
            MENU_ITEMS['requests']
        )

        # Initialize submenu items
        self.enterprise_bare_metal = EnterpriseBareMetalSubMenu(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Enterprise Bare Metal', re.I)).first,
            MENU_ITEMS['enterprise_bare_metal']
        )

        self.cloud_servers = CloudServersSubMenu(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Cloud Servers', re.I)).first,
            MENU_ITEMS['cloud_servers']
        )

        self.cloud_servers = CloudStorageSubMenu(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Cloud Servers', re.I)).first,
            MENU_ITEMS['cloud_servers']
        )

        self.networks = NetworksSubMenu(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Networks', re.I)).first,
            MENU_ITEMS['networks']
        )

        self.monitoring = MonitoringSubMenu(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Monitoring', re.I)).first,
            MENU_ITEMS['monitoring']
        )

        self.identity_and_access = IdentityAndAccessSubMenu(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Identity and Access', re.I)).first,
            MENU_ITEMS['identity_and_access']
        )

        self.billing = BillingSubMenu(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Billing', re.I)).first,
            MENU_ITEMS['billing']
        )

        self.reports = ReportsSubMenu(
            self.page,
            self.menu_list.get_by_text(re.compile(r'Reports', re.I)).first,
            MENU_ITEMS['reports']
        )

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'side menu'

    # Legacy methods for backward compatibility
    def get_menu_item(self, name: str) -> Locator:
        """Get a specific menu item locator by name."""
        return self.menu_list.locator(f'text="{name}"').first

    def get_menu_item_by_key(self, key: str) -> Locator:
        """Get menu item locator by config key."""
        return self.get_menu_item(MENU_ITEMS[key].name)

    @allure.step
    def click_menu_item(self, name: str) -> None:
        """Click on a menu item by name."""
        with allure.step(f'Click "{name}" in side menu'):
            menu_item = self.get_menu_item(name)
            menu_item.wait_for(state='visible')
            menu_item.click()
            self.page.wait_for_load_state('load')
            self.page.wait_for_timeout(2000)

    @allure.step
    def click_menu_item_by_key(self, key: str) -> None:
        """Click on a menu item by config key."""
        config = MENU_ITEMS[key]
        self.click_menu_item(config.name)

    @allure.step
    def expand_submenu(self, name: str) -> None:
        """Expand submenu by clicking on a menu item with submenu."""
        with allure.step(f'Expand "{name}" submenu'):
            menu_item = self.get_menu_item(name)
            menu_item.wait_for(state='visible')
            menu_item.click()
            self.page.wait_for_timeout(1000)

    @allure.step
    def expand_submenu_by_key(self, key: str) -> None:
        """Expand submenu by config key."""
        config = MENU_ITEMS[key]
        self.expand_submenu(config.name)

    def is_menu_item_visible(self, name: str) -> bool:
        """Check if a menu item is visible."""
        try:
            menu_item = self.get_menu_item(name)
            menu_item.wait_for(state='visible', timeout=5000)
            return True
        except:
            return False

    def is_submenu_expanded(self, name: str) -> bool:
        """Check if submenu is expanded (visible)."""
        try:
            menu_item = self.get_menu_item(name)
            submenu = menu_item.locator('..').locator('ul').first
            submenu.wait_for(state='visible', timeout=5000)
            return True
        except:
            return False

    def is_submenu_expanded_by_key(self, key: str) -> bool:
        """Check if submenu is expanded by config key."""
        config = MENU_ITEMS[key]
        return self.is_submenu_expanded(config.name)

    @allure.step
    def should_be_visible(self) -> None:
        """Verify side menu is visible."""
        with allure.step('Verify Side Menu is visible'):
            self.menu_list.wait_for(state='visible')

    @allure.step
    def get_menu_items(self) -> List[str]:
        """Get all visible menu item names."""
        with allure.step('Get all menu items'):
            items = self.menu_items.all_text_contents()
            return [item.strip() for item in items if item.strip()]

    @allure.step
    def get_submenu_items(self, parent_name: str) -> List[str]:
        """Get submenu items for a parent menu item."""
        with allure.step(f'Get submenu items for "{parent_name}"'):
            menu_item = self.get_menu_item(parent_name)
            submenu = menu_item.locator('..').locator('ul').first
            submenu.wait_for(state='visible')
            items = submenu.locator('> li').all_text_contents()
            return [item.strip() for item in items if item.strip()]

