"""Navigation tests - Python version of navigation.spec.ts

Tests for platform navigation functionality including:
- Direct menu item navigation
- Submenu item navigation and expansion
"""
import re
from typing import TypeAlias

import pytest
import allure
from playwright.sync_api import Page, expect

from src.pages.platform.dashboard_page import DashboardPage

DirectMenuCase: TypeAlias = tuple[str, str, str, str]
SubmenuCase: TypeAlias = tuple[str, str, str, str, str]

DIRECT_MENU_CASES: list[DirectMenuCase] = [
    ("Scalable Bare Metal", "Scalable Bare Metal", "sbm/welcome", "Order server"),
    ("AI compute", "AI compute", r"ai-compute/welcome", "Order"),
    ("Cloud Storage", "Cloud Storage", "cloud-storage/0/info", "Create storage"),
    ("Managed Kubernetes", "Kubernetes clusters", "k8s", "Create"),
    ("Load Balancers", "Load Balancers", "lb", "Create new balancer"),
    ("Firewalls", "Firewalls", "firewalls", "Create"),
    ("Private Racks", "Private Racks", "private-racks", "Order rack"),
    ("SSL certificates", "SSL certificates", "ssl", "Create"),
    ("Account settings", "Account settings", "account", "Create"),
    ("Requests", "Requests", "requests", "Submit a new request"),
]

SUBMENU_CASES: list[SubmenuCase] = [
    ("Enterprise Bare Metal", "Manage", "Manage", "servers/my", "My servers"),
    ("Enterprise Bare Metal", "Order", "Order", "servers/order", "Reset filter"),
    ("Cloud Servers", "Create & Manage", "Cloud Servers", r"cloud-computing\?page=1", "Create server"),
    ("Cloud Servers", "Snapshots & Backups", "Snapshots & Backups", "cloud-computing/snapshots", "Snapshots & Backups"),
    ("Cloud Servers", "Images", "Images", "cloud-computing/images", "Refresh"),
    ("Cloud Servers", "Volumes", "Volumes", "cloud-computing/block-storage/info", "Create volume"),
    ("Networks", "Direct Connect", "Direct Connect", "networks/dc", "Add connection"),
    ("Networks", "L2 Segments", "L2 Segments", "networks/l2", "Add segment"),
    ("Networks", "DNS", "DNS", "networks/dns", "Add domain"),
    ("Networks", "VPN access", "VPN access", "networks/vpn", "Create"),
    ("Monitoring", "Healthchecks", "Healthchecks", "monitoring/healthchecks", "Add new healthcheck"),
    ("Monitoring", "Notifications", "Notifications", "monitoring/notifications", "Add new notification group"),
    ("Identity and Access", "SSH & GPG keys", "SSH & GPG keys", "iam/keys", "Create"),
    ("Identity and Access", "API tokens", "API tokens", "iam/api-tokens", "Create"),
    ("Billing", "Orders", "Orders", "billing/orders", "Pending"),
    ("Billing", "Invoices", "Invoices", "billing/invoices", "Invoices"),
    ("Billing", "Group invoices", "Group invoices", "billing/group-invoices", "Create group"),
    ("Billing", "Account statement", "Account statement", "billing/statement", "Print"),
    ("Billing", "Payment details", "Payment details", "payment/methods", "Add new card"),
    ("Billing", "Top up balance", "Top up balance", "payment/pay", "Proceed"),
]


@pytest.mark.timeout(90)
class TestNavigationDirectMenuItems:
    """Navigation Tests - Direct Menu Items"""

    @pytest.mark.parametrize(
        "menu_item, header, url_regex, button_name",
        DIRECT_MENU_CASES,
    )
    def test_direct_menu_items(
        self,
        authorized_page: Page,
        menu_item: str,
        header: str,
        url_regex: str,
        button_name: str,
    ) -> None:
        """Test direct menu item navigation for all main items."""
        dashboard_page = DashboardPage(authorized_page)
        dashboard_page.open()

        with allure.step(f"Navigate to Direct Menu Item - {menu_item}"):
            dashboard_page.side_menu.click_menu_item(menu_item)

        with allure.step("Verify destination page"):
            dashboard_page.get_by_role("button", name=button_name).first.wait_for(state="visible")

            expect(authorized_page).to_have_url(re.compile(f'/a:\\w+/{url_regex}$'))
            expect(authorized_page.get_by_role('heading', name=header, exact=True).first).to_be_visible()


@pytest.mark.timeout(90)
class TestNavigationSubmenuItems:
    """Test menu item navigation for all items with submenus, verifying that submenus can be expanded and navigated to."""

    @pytest.mark.parametrize(
        "main_item, submenu_item, header, url_regex, element_name",
        SUBMENU_CASES,
    )
    def test_submenu_items(
        self,
        authorized_page: Page,
        main_item: str,
        submenu_item: str,
        header: str,
        url_regex: str,
        element_name: str,
    ) -> None:
        """Test that submenu items can be expanded and navigated to."""
        verify_by_h2 = header in ["Manage", "Snapshots & Backups", "Invoices"]  # These pages use h2 for main header instead of h1
        dashboard_page = DashboardPage(authorized_page)
        dashboard_page.open()

        with allure.step(f"Navigate to {main_item} > {submenu_item}"):
            dashboard_page.side_menu.click_menu_item(main_item)

            # Click the specific subitem
            dashboard_page.side_menu.click_menu_item(submenu_item)

        with allure.step(f"Verify {submenu_item} page loaded"):
            expect(authorized_page).to_have_url(re.compile(f'/a:\\w+/{url_regex}'))
            expect(authorized_page.get_by_role('heading', name=header).first).to_be_visible()
            if verify_by_h2:
                expect(authorized_page.get_by_role('heading', name=element_name, exact=True).first).to_be_visible()
            else:
                expect(authorized_page.get_by_role("button", name=element_name).first).to_be_visible()
