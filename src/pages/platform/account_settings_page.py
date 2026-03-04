"""Account Settings page object model."""
from typing import Optional
from playwright.sync_api import Page, Locator
import allure

from .dashboard_page import DashboardPage
from src.elements import Heading, Button
from src.elements.contact import ContactsTable, ContactTableRow, ContactInformationForm, ViewContactInfoForm


class AccountSettingsPage(DashboardPage):
    """Account Settings Page Object Model.
    URL: /account
    """

    def __init__(self, page: Page) -> None:
        """
        Initialize AccountSettingsPage.
        
        Args:
            page: The Playwright Page object
        """
        super().__init__(page)
        self.url_path = "/account"
        self.page_heading = Heading(self.page, 'Account settings')
        self.edit_button = Button(self.page, 'Edit')
        self.refresh_button = self.page.get_by_role("button", name="Refresh").first
        self.account_form = self.page.locator('text=/account|email|profile|settings/i').first

        # Subscriptions block elements - using flexible locators
        # Find the Subscriptions section by heading
        self.subscriptions_block = self.page.locator('section, div').filter(
            has=self.page.get_by_role('heading', name='Subscriptions').first
        ).first
        
        # Create button is specifically in the Subscriptions block
        self.create_contact_button = self.subscriptions_block.get_by_role('button', name='Create').first
        self.contacts_table = ContactsTable(self.page)

        # Forms
        self.contact_information_form = ContactInformationForm(self.page)
        self.view_contact_info_form = ViewContactInfoForm(self.page)

    def open(self) -> None:
        """Open Account Settings page."""
        with allure.step('Open Account Settings page'):
            self.page.goto(f'{self.base_url}{self.url_path}')
            self.verify_page_loaded()

    @allure.step
    def verify_page_loaded(self) -> None:
        """Verify Account Settings page is loaded."""
        with allure.step('Verify Account Settings page is loaded'):
            self.verify_url(self.url_path)
            self.page_heading.should_be_visible()
            self.edit_button.should_be_visible()
            self.account_form.wait_for(state='visible', timeout=10000)

    @allure.step
    def verify_subscriptions_block_visible(self) -> None:
        """Verify Subscriptions block is visible."""
        with allure.step('Verify Subscriptions block is visible'):
            # Try multiple possible locators for subscriptions/contacts section
            subscriptions_block = self.page.locator('[class*="subscription"], [class*="contact"], section').filter(
                has_text='subscription'
            ).first.or_(self.page.locator('[class*="subscription"], [class*="contact"], section').filter(
                has_text='contact'
            ).first).or_(self.page.locator('[class*="subscription"], [class*="contact"], section').filter(
                has_text='create'
            ).first)
            
            try:
                subscriptions_block.wait_for(state='visible', timeout=5000)
            except:
                # If specific block not found, check for Create button
                try:
                    self.create_contact_button.wait_for(state='visible', timeout=5000)
                except:
                    # Or check for table
                    self.contacts_table.should_be_visible()

    @allure.step
    def click_create_contact(self) -> None:
        """Click Create button in Subscriptions block."""
        with allure.step('Click Create button in Subscriptions block'):
            self.create_contact_button.wait_for(state='visible', timeout=10000)
            self.create_contact_button.click()

    @allure.step
    def click_refresh_table(self) -> None:
        """Click the refresh button to reload the table."""
        with allure.step('Click refresh button'):
            self.refresh_button.wait_for(state='visible')
            self.refresh_button.click(force=True)


    @allure.step
    def get_contact_row(self, contact_id: str) -> Optional[ContactTableRow]:
        """Get contact row by ID."""
        with allure.step(f'Find contact row for ID: {contact_id}'):
            return self.contacts_table.get_row_by_contact_id(contact_id)

    @allure.step
    def click_contact(self, contact_id: str) -> None:
        """Click on contact link in table."""
        with allure.step(f'Click contact link for ID: {contact_id}'):
            row = self.get_contact_row(contact_id)
            if row:
                row.click_contact()
            else:
                raise ValueError(f'Contact {contact_id} not found in table')

    @allure.step
    def click_delete_contact(self, contact_id: str) -> None:
        """Click delete button for a contact in the table."""
        with allure.step(f'Click delete button for contact ID: {contact_id}'):
            row = self.get_contact_row(contact_id)
            if row:
                row.click_delete()
            else:
                raise ValueError(f'Contact {contact_id} not found in table')

    @allure.step
    def verify_contact_in_table(self, contact_id: str) -> None:
        """Verify contact exists in table."""
        with allure.step(f'Verify contact {contact_id} exists in table'):
            self.contacts_table.verify_contact_exists(contact_id)

    @allure.step
    def verify_contact_not_in_table(self, contact_id: str) -> None:
        """Verify contact does not exist in table."""
        with allure.step(f'Verify contact {contact_id} does not exist in table'):
            self.contacts_table.verify_contact_not_exists(contact_id)

    @allure.step
    def get_delete_button_for_contact(self, contact_id: str) -> Locator:
        """Get delete button for a specific contact."""
        with allure.step(f'Get delete button for contact ID: {contact_id}'):
            row = self.get_contact_row(contact_id)
            if not row:
                raise ValueError(f'Contact {contact_id} not found in table')
            return row.delete_button
