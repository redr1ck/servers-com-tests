"""Managed Kubernetes page object model."""
from playwright.sync_api import Page
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, MENU_ITEMS


class ManagedKubernetesPage(DashboardPage):
    """Managed Kubernetes Page Object Model.
    URL: /k8s
    """

    def __init__(self, page: Page):
        """
        Initialize ManagedKubernetesPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.base_url += "/k8s"
        self.page_heading = Heading(page, 'Managed Kubernetes')

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Managed Kubernetes page is loaded."""
        with allure.step('Verify Managed Kubernetes page is loaded'):
            self.verify_url('/k8s')
            self.page_heading.should_be_visible()
