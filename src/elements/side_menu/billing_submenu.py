"""Billing submenu class."""
import re
from playwright.sync_api import Page, Locator
from .submenu import SubMenu
from .menu_item import MenuItem
from .menu_item_config import MenuItemConfig


class BillingSubMenu(SubMenu):
    """Billing submenu with specific items."""

    def __init__(self, page: Page, locator: Locator, config: MenuItemConfig):
        super().__init__(page, locator, config)

        self.orders = MenuItem(
            page,
            page.get_by_role('link', name='Orders').first,
            MenuItemConfig('Orders', '/billing/orders', False)
        )

        self.invoices = MenuItem(
            page,
            page.get_by_role('link', name='Invoices').first,
            MenuItemConfig('Invoices', '/billing/invoices', False)
        )

        self.group_invoices = MenuItem(
            page,
            page.get_by_role('link', name=re.compile(r'Group.*invoices', re.I)),
            MenuItemConfig('Group invoices', '/billing/group-invoices', False)
        )

        self.account_statement = MenuItem(
            page,
            page.get_by_role('link', name=re.compile(r'Account.*statement', re.I)),
            MenuItemConfig('Account statement', '/billing/statement', False)
        )

        self.payment_details = MenuItem(
            page,
            page.get_by_role('link', name=re.compile(r'Payment.*details', re.I)),
            MenuItemConfig('Payment details', '/payment/methods', False)
        )

        self.top_up_balance = MenuItem(
            page,
            page.get_by_role('link', name=re.compile(r'Top.*up.*balance', re.I)),
            MenuItemConfig('Top up balance', '/payment/pay', False)
        )

