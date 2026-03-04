"""Contact table row element classes."""
from typing import Optional, List
from playwright.sync_api import Page, Locator, expect
import allure
from ..base_element import BaseElement
from src.utils.decorators import retry_on_condition


class ContactTableRow(BaseElement):
    """Represents a contact row in the subscriptions/contacts table."""

    def __init__(self, row: Locator):
        """
        Initialize a ContactTableRow element.
        
        Args:
            row: The Playwright Locator for the table row
        """
        super().__init__(row.page, row, 'Contact Table Row')

        self.contact_link = row.locator('a[href*="/account/contact/"]').first
        self.name_cell = row.locator('[class*="name"], td:first-child').first
        self.type_cell = row.locator('[class*="type"]').first
        self.email_cell = row.locator('[class*="email"]').first
        self.phone_cell = row.locator('[class*="phone"]').first
        # Delete button is the last button in the row (icon button without text)
        self.delete_button = row.locator('button').last

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'table row'

    @allure.step
    def click_contact(self) -> None:
        """Click on the contact link to navigate to contact detail page."""
        with allure.step('Click contact link'):
            self.contact_link.wait_for(state='visible', timeout=10000)
            self.contact_link.click()

    @allure.step
    def click_delete(self) -> None:
        """Click delete button for this contact."""
        with allure.step('Click delete button'):
            self.delete_button.wait_for(state='visible', timeout=10000)
            self.delete_button.click()

    @allure.step
    def get_contact_id(self) -> Optional[str]:
        """Get contact ID from href."""
        with allure.step('Get contact ID'):
            href = self.contact_link.get_attribute('href')
            return href.split('/')[-1] if href else None

    @allure.step
    def should_be_visible(self) -> None:
        """Verify row is visible."""
        with allure.step('Verify contact row is visible'):
            self.element_locator.wait_for(state='visible', timeout=10000)

    @allure.step
    def should_contain_text(self, text: str) -> None:
        """Verify row contains expected text."""
        with allure.step(f'Verify row contains text: {text}'):
            expect(self.element_locator).to_contain_text(text)


class ContactsTable(BaseElement):
    """Represents the contacts table in Account Settings page."""

    def __init__(self, page: Page):
        """
        Initialize a ContactsTable element.
        
        Args:
            page: The Playwright Page object
        """
        table_locator = page.locator('table, [role="table"], [class*="table"]').first
        super().__init__(page, table_locator, 'Contacts Table')


        # Reliable row selector - find rows with contact links
        self.rows = self.element_locator.locator('tr:has(a[href*="/account/contact/"])')

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'table'

    @allure.step
    def get_rows(self) -> List[ContactTableRow]:
        """Get all contact rows."""
        with allure.step('Get all contact rows'):
            rows = self.rows.all()
            return [ContactTableRow(row) for row in rows]

    @allure.step
    def get_row_by_contact_id(self, contact_id: str) -> Optional[ContactTableRow]:
        """Get row by contact ID."""
        with allure.step(f'Get row by contact ID: {contact_id}'):
            rows = self.get_rows()
            for row in rows:
                row_id = row.get_contact_id()
                if row_id == contact_id:
                    return row
            return None

    @allure.step
    def verify_contact_exists(self, contact_id: str) -> None:
        """Verify contact exists in table."""
        with allure.step(f'Verify contact {contact_id} exists in table'):
            row = self.get_row_by_contact_id(contact_id)
            if not row:
                # Get all available contact IDs for debugging
                rows = self.get_rows()
                available_ids = []
                for r in rows:
                    try:
                        row_id = r.get_contact_id()
                        if row_id:
                            available_ids.append(row_id)
                    except:
                        pass  # Skip rows without valid contact links
                        
                raise AssertionError(
                    f'Contact {contact_id} not found in table. '
                    f'Available contacts: {", ".join(available_ids) if available_ids else "none"}'
                )
            row.should_be_visible()

    @allure.step
    def verify_contact_not_exists(self, contact_id: str) -> None:
        """Verify contact does not exist in table."""
        with allure.step(f'Verify contact {contact_id} does not exist in table'):
            # Wait for table to update (DOM refresh after delete)
            self.page.wait_for_load_state('networkidle', timeout=10000)
            self.page.wait_for_timeout(500)  # Additional wait for DOM updates

            @retry_on_condition(
                page=self.page,
                max_retries=3,
                wait_ms=1000,
                condition_func=lambda row: row is not None
            )
            def _check_contact_deleted() -> Optional[ContactTableRow]:
                """Returns None if contact is deleted, ContactTableRow if still exists."""
                return self.get_row_by_contact_id(contact_id)

            result = _check_contact_deleted()
            if result:
                raise AssertionError(f'Contact {contact_id} still exists in table after delete')

    @allure.step
    def get_row_count(self) -> int:
        """Get row count."""
        with allure.step('Get row count'):
            return self.rows.count()

    @allure.step
    def should_be_visible(self) -> None:
        """Verify table is visible."""
        with allure.step('Verify contacts table is visible'):
            self.element_locator.wait_for(state='visible', timeout=10000)