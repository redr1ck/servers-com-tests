"""Navigation tests - Python version of navigation.spec.ts

Tests for platform navigation functionality including:
- Direct menu item navigation
- Submenu item navigation and expansion
"""
import re
import pytest
import allure
from playwright.sync_api import Page, expect

from src.pages.platform.dashboard_page import DashboardPage


@pytest.mark.timeout(90)
class TestNavigationDirectMenuItems:
    """Navigation Tests - Direct Menu Items"""
    @pytest.mark.parametrize("menu_item, header, url_regex, button_name",[
    ("Scalable Bare Metal", "Scalable Bare Metal", "sbm/welcome", "Order server"),
    ("AI compute", "AI compute", r"ai-compute/welcome", "Order"),
    ("Cloud Storage", "Cloud Storage", "cloud-storage/0/info", "Create storage"),
    ("Managed Kubernetes", "Kubernetes clusters", "k8s", "Create"),
    ("Load Balancers", "Load Balancers", "lb", "Create new balancer"),
    ("Firewalls", "Firewalls", "firewalls", "Create"),
    ("Private Racks", "Private Racks", "private-racks", "Order rack"),
    ("SSL certificates", "SSL certificates", "ssl", "Create"),
    ("Account settings", "Account settings", "account", "Create"),
    ("Requests", "Requests", "requests", "Submit a new request")
])
    def test_direct_menu_items(self, authorized_page: Page, menu_item, header, url_regex, button_name):
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

    @pytest.mark.parametrize("main_item, submenu_item, header, url_regex, element_name", [
        # Enterprise Bare Metal
        ("Enterprise Bare Metal", "Manage", "Manage", "servers/my", "My servers"),  # h2
        ("Enterprise Bare Metal", "Order", "Order", "servers/order", "Reset filter"),

        # Cloud Servers
        ("Cloud Servers", "Create & Manage", "Cloud Servers", r"cloud-computing\?page=1", "Create server"),
        ("Cloud Servers", "Snapshots & Backups", "Snapshots & Backups", "cloud-computing/snapshots", "Snapshots & Backups"),  # h2
        ("Cloud Servers", "Images", "Images", "cloud-computing/images", "Refresh"),
        ("Cloud Servers", "Volumes", "Volumes", "cloud-computing/block-storage/info", "Create volume"),

        # Networks
        ("Networks", "Direct Connect", "Direct Connect", "networks/dc", "Add connection"),
        ("Networks", "L2 Segments", "L2 Segments", "networks/l2", "Add segment"),
        ("Networks", "DNS", "DNS", "networks/dns", "Add domain"),
        ("Networks", "VPN access", "VPN access", "networks/vpn", "Create"),

        # Monitoring
        ("Monitoring", "Healthchecks", "Healthchecks", "monitoring/healthchecks", "Add new healthcheck"),
        ("Monitoring", "Notifications", "Notifications", "monitoring/notifications", "Add new notification group"),

        # Identity and Access
        ("Identity and Access", "SSH & GPG keys", "SSH & GPG keys", "iam/keys", "Create"),
        ("Identity and Access", "API tokens", "API tokens", "iam/api-tokens", "Create"),

        # Billing
        ("Billing", "Orders", "Orders", "billing/orders", "Pending"),
        ("Billing", "Invoices", "Invoices", "billing/invoices", "Invoices"),  # h2
        ("Billing", "Group invoices", "Group invoices", "billing/group-invoices", "Create group"),
        ("Billing", "Account statement", "Account statement", "billing/statement", "Print"),
        ("Billing", "Payment details", "Payment details", "payment/methods", "Add new card"),
        ("Billing", "Top up balance", "Top up balance", "payment/pay", "Proceed"),
    ])
    def test_submenu_items(self, authorized_page: Page, main_item, submenu_item, header, url_regex, element_name):
        """Test that submenu items can be expanded and navigated to."""
        verify_by_h2 = header in ["Manage", "Snapshots & Backups", "Invoices"]  # These pages use h2 for main header instead of h1
        dashboard_page = DashboardPage(authorized_page)
        dashboard_page.open()

        with allure.step(f"Navigate to {main_item} > {submenu_item}"):
            dashboard_page.side_menu.click_menu_item(main_item)
            # authorized_page.wait_for_load_state('networkidle')

            # Click the specific subitem
            dashboard_page.side_menu.click_menu_item(submenu_item)
            # authorized_page.wait_for_load_state('networkidle')

        with allure.step(f"Verify {submenu_item} page loaded"):
            expect(authorized_page).to_have_url(re.compile(f'/a:\\w+/{url_regex}'))
            expect(authorized_page.get_by_role('heading', name=header).first).to_be_visible()
            if verify_by_h2:
                expect(authorized_page.get_by_role('heading', name=element_name, exact=True).first).to_be_visible()
            else:
                # dashboard_page.get_by_role("button", name=element_name).first.wait_for(state="visible", timeout=10000)
                expect(authorized_page.get_by_role("button", name=element_name).first).to_be_visible()
