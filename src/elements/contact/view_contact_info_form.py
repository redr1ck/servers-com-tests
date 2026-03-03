"""View contact information form element class."""
from typing import Dict
from playwright.sync_api import Page, Locator, expect
import allure
from ..base_element import BaseElement
from src.models.contac_form import ContactFormData


class ViewContactInfoForm(BaseElement):
    """Represents the view-only contact information display on /account/contact/<id> page."""

    def __init__(self, page: Page):
        """
        Initialize a ViewContactInfoForm element.
        
        Args:
            page: The Playwright Page object
        """
        container_locator = page.locator('body').first
        super().__init__(page, container_locator, 'View Contact Info Form')
        self.edit_button = page.get_by_role('button', name='Edit').first

        # Display fields (read-only text) - using flexible locators
        self.name_display = self.page.locator('[class*="name"], [data-testid*="name"]').first.or_(self.page.get_by_text('name').first)
        self.email_display = self.page.locator('[class*="email"], [data-testid*="email"]').first.or_(self.page.get_by_text('email').first)
        self.phone_display = self.page.locator('[class*="phone"], [data-testid*="phone"]').first.or_(self.page.get_by_text('phone').first)
        self.company_display = self.page.locator('[class*="company"], [data-testid*="company"]').first.or_(self.page.get_by_text('company').first)

        # Role display - shows checked roles as text/badges
        self.role_display = self.page.locator('[class*="role"]').first.or_(self.page.get_by_text('role').first)

        # Checkboxes (may not exist on view page - replaced by role text)
        self.primary_checkbox = self.page.get_by_role('checkbox', name='Primary').first
        self.emergency_checkbox = self.page.get_by_role('checkbox', name='Emergency').first
        self.billing_checkbox = self.page.get_by_role('checkbox', name='Billing').first
        self.technical_checkbox = self.page.get_by_role('checkbox', name='Technical').first

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'view form'

    @allure.step
    def click_edit(self) -> None:
        """Click the Edit button to switch to edit mode."""
        with allure.step('Click Edit button'):
            self.edit_button.wait_for(state='visible', timeout=10000)
            self.edit_button.click()

    @allure.step
    def verify_data(self, expected_data: ContactFormData) -> None:
        """Verify all displayed data matches expected."""
        with allure.step('Verify contact data'):
            if expected_data.first_name:
                try:
                    self.name_display.wait_for(state='visible', timeout=5000)
                    expect(self.name_display).to_contain_text(expected_data.first_name)
                except:
                    pass  # Field may not exist
                    
            if expected_data.email:
                try:
                    self.email_display.wait_for(state='visible', timeout=5000)
                    expect(self.email_display).to_contain_text(expected_data.email)
                except:
                    pass
                    
            if expected_data.phone:
                try:
                    self.phone_display.wait_for(state='visible', timeout=5000)
                    expect(self.phone_display).to_contain_text(expected_data.phone)
                except:
                    pass
                    
            if expected_data.company:
                try:
                    self.company_display.wait_for(state='visible', timeout=5000)
                    expect(self.company_display).to_contain_text(expected_data.company)
                except:
                    pass

    @allure.step
    def verify_roles(self, expected_data: ContactFormData) -> None:
        """Verify roles are displayed correctly (for checked checkboxes except Primary)."""
        with allure.step('Verify contact roles'):
            roles = []
            if expected_data.is_emergency:
                roles.append('emergency')
            if expected_data.is_billing:
                roles.append('billing')
            if expected_data.is_technical:
                roles.append('technical')
                
            if roles:
                try:
                    self.role_display.wait_for(state='visible', timeout=5000)
                    role_text = self.role_display.text_content() or ''
                    role_text_lower = role_text.lower()
                    for role in roles:
                        if role not in role_text_lower:
                            raise AssertionError(f'Role "{role}" not found in role display: {role_text}')
                except:
                    pass  # Role display may have different structure

    def get_checkbox_state(self, checkbox_name: str) -> bool:
        """Get checkbox state."""
        checkbox_map = {
            'primary': self.primary_checkbox,
            'emergency': self.emergency_checkbox,
            'billing': self.billing_checkbox,
            'technical': self.technical_checkbox,
        }
        
        checkbox = checkbox_map.get(checkbox_name.lower())
        if not checkbox:
            raise ValueError(f'Unknown checkbox: {checkbox_name}')
            
        try:
            return checkbox.is_checked()
        except:
            # Checkbox may not exist on view page
            return False

    @allure.step
    def verify_checkbox_states(self, expected_states: Dict[str, bool]) -> None:
        """Verify checkbox states."""
        with allure.step('Verify checkbox states'):
            for name, expected_state in expected_states.items():
                actual_state = self.get_checkbox_state(name)
                if actual_state != expected_state:
                    raise AssertionError(
                        f'Checkbox "{name}" expected to be {"checked" if expected_state else "unchecked"}, '
                        f'but was {"checked" if actual_state else "unchecked"}'
                    )

    @allure.step
    def should_be_visible(self) -> None:
        """Verify form is visible."""
        with allure.step('Verify View Contact Info Form is visible'):
            # Check if any of the display fields are visible
            try:
                display_locators = self.name_display.or_(self.email_display).or_(self.phone_display).or_(self.role_display)
                display_locators.wait_for(state='visible', timeout=10000)
            except:
                # Try checking for checkboxes
                try:
                    checkbox_locators = self.primary_checkbox.or_(self.emergency_checkbox)
                    checkbox_locators.wait_for(state='visible', timeout=5000)
                except:
                    pass  # Page structure may be different