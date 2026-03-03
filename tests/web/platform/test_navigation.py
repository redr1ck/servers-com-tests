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
from src.pages.platform.scalable_bare_metal_page import ScalableBareMetalPage
from src.pages.platform.ai_compute_page import AIComputePage
from src.pages.platform.cloud_storage_page import CloudStoragePage
from src.pages.platform.managed_kubernetes_page import ManagedKubernetesPage
from src.pages.platform.load_balancers_page import LoadBalancersPage
from src.pages.platform.firewalls_page import FirewallsPage
from src.pages.platform.private_racks_page import PrivateRacksPage
from src.pages.platform.ssl_certificates_page import SSLCertificatesPage
from src.pages.platform.account_settings_page import AccountSettingsPage
from src.pages.platform.requests_page import RequestsPage
from src.pages.platform.enterprise_bare_metal_page import EnterpriseBareMetalPage
from src.pages.platform.cloud_servers_page import CloudServersPage
from src.pages.platform.networks_page import NetworksPage
from src.pages.platform.monitoring_page import MonitoringPage
from src.pages.platform.identity_and_access_page import IdentityAndAccessPage
from src.pages.platform.billing_page import BillingPage
from src.pages.platform.reports_page import ReportsPage

@pytest.mark.timeout(90)
class TestNavigationDirectMenuItems:
    """Navigation Tests - Direct Menu Items"""

    def test_tc_nav_001_scalable_bare_metal(self, authorized_page: Page):
        """TC-NAV-001: Scalable Bare Metal"""
        with allure.step("Navigate to Scalable Bare Metal"):
            sbm_page = ScalableBareMetalPage(authorized_page)
            sbm_page.open()
            sbm_page.side_menu.scalable_bare_metal.click()
            sbm_page.verify_page_loaded()
            sbm_page.verify_header_visible()

    def test_tc_nav_003_ai_compute(self, authorized_page: Page):
        """TC-NAV-003: AI compute"""
        with allure.step("Navigate to AI compute"):
            ai_page = AIComputePage(authorized_page)
            ai_page.side_menu.ai_compute.click()
            ai_page.verify_page_loaded()
            ai_page.verify_header_visible()

    def test_tc_nav_006_managed_kubernetes(self, authorized_page: Page):
        """TC-NAV-006: Managed Kubernetes"""
        with allure.step("Navigate to Managed Kubernetes"):
            k8s_page = ManagedKubernetesPage(authorized_page)
            k8s_page.side_menu.managed_kubernetes.click()
            k8s_page.verify_page_loaded()
            k8s_page.verify_header_visible()

    def test_tc_nav_007_load_balancers(self, authorized_page: Page):
        """TC-NAV-007: Load Balancers"""
        with allure.step("Navigate to Load Balancers"):
            lb_page = LoadBalancersPage(authorized_page)
            lb_page.side_menu.load_balancers.click()
            lb_page.verify_page_loaded()
            lb_page.verify_header_visible()

    def test_tc_nav_008_firewalls(self, authorized_page: Page):
        """TC-NAV-008: Firewalls"""
        with allure.step("Navigate to Firewalls"):
            fw_page = FirewallsPage(authorized_page)
            fw_page.side_menu.firewalls.click()
            fw_page.verify_page_loaded()
            fw_page.verify_header_visible()

    def test_tc_nav_010_private_racks(self, authorized_page: Page):
        """TC-NAV-010: Private Racks"""
        with allure.step("Navigate to Private Racks"):
            racks_page = PrivateRacksPage(authorized_page)
            racks_page.side_menu.private_racks.click()
            racks_page.verify_page_loaded()
            racks_page.verify_header_visible()

    def test_tc_nav_012_ssl_certificates(self, authorized_page: Page):
        """TC-NAV-012: SSL certificates"""
        with allure.step("Navigate to SSL certificates"):
            ssl_page = SSLCertificatesPage(authorized_page)
            ssl_page.side_menu.ssl_certificates.click()
            ssl_page.verify_page_loaded()
            ssl_page.verify_header_visible()

    def test_tc_nav_005_cloud_storage(self, authorized_page: Page):
        """TC-NAV-005: Cloud Storage"""
        with allure.step("Navigate to Cloud Storage"):
            storage_page = CloudStoragePage(authorized_page)
            storage_page.side_menu.cloud_storage.click()
            storage_page.verify_page_loaded()
            storage_page.verify_header_visible()

    def test_tc_nav_013_account_settings(self, authorized_page: Page):
        """TC-NAV-013: Account settings"""
        with allure.step("Navigate to Account settings"):
            account_page = AccountSettingsPage(authorized_page)
            account_page.side_menu.account_settings.click()
            account_page.verify_page_loaded()
            account_page.verify_header_visible()

    def test_tc_nav_017_requests(self, authorized_page: Page):
        """TC-NAV-017: Requests"""
        with allure.step("Navigate to Requests"):
            requests_page = RequestsPage(authorized_page)
            requests_page.side_menu.requests.click()
            requests_page.verify_page_loaded()
            requests_page.verify_header_visible()


@pytest.mark.timeout(90)
class TestNavigationSubmenuItems:
    """Navigation Tests - Submenu Item Navigation"""

    def test_tc_nav_002_sub_enterprise_bare_metal(self, authorized_page: Page):
        """TC-NAV-002-SUB: Enterprise Bare Metal - navigate to submenu items"""
        with allure.step("Navigate to Enterprise Bare Metal submenu items"):
            dashboard_page = DashboardPage(authorized_page)
            dashboard_page.open()
            # Expand Enterprise Bare Metal submenu
            dashboard_page.side_menu.enterprise_bare_metal.click()
            authorized_page.wait_for_load_state('networkidle')

            # Verify navigation
            current_url = authorized_page.url
            assert 'servers' in current_url.lower(), f"Expected servers in URL, got: {current_url}"

    def test_tc_nav_004_sub_cloud_servers(self, authorized_page: Page):
        """TC-NAV-004-SUB: Cloud Servers - navigate to submenu items"""
        with allure.step("Navigate to Cloud Servers submenu items"):
            dashboard_page = DashboardPage(authorized_page)
            dashboard_page.open()
            # Expand Cloud Servers submenu
            dashboard_page.side_menu.cloud_servers.click()
            authorized_page.wait_for_load_state('networkidle')

            # Verify navigation
            current_url = authorized_page.url
            assert 'cloud' in current_url.lower(), f"Expected cloud in URL, got: {current_url}"

    def test_tc_nav_005_sub_cloud_storage(self, authorized_page: Page):
        """TC-NAV-005-SUB: Cloud Storage - navigate to submenu items"""
        with allure.step("Navigate to Cloud Storage submenu items"):
            dashboard_page = DashboardPage(authorized_page)
            dashboard_page.open()

            # Expand Cloud Storage submenu
            dashboard_page.side_menu.cloud_storage.click()
            authorized_page.wait_for_load_state('networkidle')

            # Verify navigation
            current_url = authorized_page.url
            assert 'storage' in current_url.lower() or 'cloud' in current_url.lower(), f"Expected storage/cloud in URL, got: {current_url}"

    def test_tc_nav_009_sub_networks(self, authorized_page: Page):
        """TC-NAV-009-SUB: Networks - navigate to submenu items"""
        with allure.step("Navigate to Networks submenu items"):
            dashboard_page = DashboardPage(authorized_page)
            dashboard_page.open()

            # Expand Networks submenu
            dashboard_page.side_menu.networks.click()
            authorized_page.wait_for_load_state('networkidle')

            # Verify navigation
            current_url = authorized_page.url
            assert 'network' in current_url.lower() or 'k8s' in current_url.lower(), f"Expected network/k8s in URL, got: {current_url}"

    def test_tc_nav_011_sub_monitoring(self, authorized_page: Page):
        """TC-NAV-011-SUB: Monitoring - navigate to submenu items"""
        with allure.step("Navigate to Monitoring submenu items"):
            dashboard_page = DashboardPage(authorized_page)
            dashboard_page.open()

            # Expand Monitoring submenu
            dashboard_page.side_menu.monitoring.click()
            authorized_page.wait_for_load_state('networkidle')

            # Verify navigation
            current_url = authorized_page.url
            assert 'monitoring' in current_url.lower(), f"Expected monitoring in URL, got: {current_url}"

    def test_tc_nav_014_sub_identity_and_access(self, authorized_page: Page):
        """TC-NAV-014-SUB: Identity and Access - navigate to submenu items"""
        with allure.step("Navigate to Identity and Access submenu items"):
            dashboard_page = DashboardPage(authorized_page)
            dashboard_page.open()

            # Expand Identity and Access submenu
            dashboard_page.side_menu.identity_and_access.click()
            authorized_page.wait_for_load_state('networkidle')

            # Verify navigation
            current_url = authorized_page.url
            assert 'iam' in current_url.lower() or 'identity' in current_url.lower(), f"Expected iam/identity in URL, got: {current_url}"

    def test_tc_nav_015_sub_billing(self, authorized_page: Page):
        """TC-NAV-015-SUB: Billing - navigate to submenu items"""
        with allure.step("Navigate to Billing submenu items"):
            dashboard_page = DashboardPage(authorized_page)
            dashboard_page.open()

            # Expand Billing submenu
            dashboard_page.side_menu.billing.click()
            authorized_page.wait_for_load_state('networkidle')

            # Verify navigation
            current_url = authorized_page.url
            assert 'billing' in current_url.lower() or 'payment' in current_url.lower(), f"Expected billing/payment in URL, got: {current_url}"

    def test_tc_nav_016_sub_reports(self, authorized_page: Page):
        """TC-NAV-016-SUB: Reports - navigate to submenu items"""
        with allure.step("Navigate to Reports submenu items"):
            dashboard_page = DashboardPage(authorized_page)
            # Expand Reports submenu
            dashboard_page.side_menu.reports.click()
            authorized_page.wait_for_load_state('networkidle')

            # Verify navigation
            current_url = authorized_page.url
            assert 'report' in current_url.lower(), f"Expected report in URL, got: {current_url}"
