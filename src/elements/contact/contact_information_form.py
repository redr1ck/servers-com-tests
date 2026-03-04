"""Contact information form element class."""
from playwright.sync_api import Page
import allure
from ..base_element import BaseElement
from src.models.contac_form import ContactFormData


class ContactInformationForm(BaseElement):
    """Represents the contact information form on /account/new-contact and /account/contact/<id> pages."""

    def __init__(self, page: Page) -> None:
        """
        Initialize a ContactInformationForm element.
        
        Args:
            page: The Playwright Page object
        """
        form_locator = page.locator('form').first
        super().__init__(page, form_locator, 'Contact Information Form')

        # Text inputs
        self.name_input = self.page.get_by_role('textbox', name='Name').or_(self.page.get_by_role('textbox', name='First name')).first
        self.last_name_input = self.page.get_by_role('textbox', name='Last name').first
        self.email_input = self.page.get_by_role('textbox', name='Email').or_(self.page.get_by_role('textbox', name='Primary email')).first
        self.secondary_email_input = self.page.get_by_role('textbox', name='Secondary email').first
        self.phone_input = self.page.get_by_role('textbox', name='Phone').first
        self.company_input = self.page.get_by_role('textbox', name='Company').first
        self.job_title_input = self.page.get_by_role('textbox', name='Job title').first
        self.comment_input = self.page.get_by_role('textbox', name='Comment').or_(self.page.locator('textarea[placeholder*="comment"], input[placeholder*="comment"]')).first

        # Checkboxes
        self.primary_checkbox = self.page.get_by_role('checkbox', name='Primary').first
        self.emergency_checkbox = self.page.get_by_role('checkbox', name='Emergency').first
        self.billing_checkbox = self.page.get_by_role('checkbox', name='Billing').first
        self.technical_checkbox = self.page.get_by_role('checkbox', name='Technical').first
        self.abuse_checkbox = self.page.get_by_role('checkbox', name='Abuse').first

        # Action buttons
        self.create_button = page.get_by_role('button', name='Create').first
        self.save_button = page.get_by_role('button', name='Save').first

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'form'

    @allure.step
    def fill_all_fields(self, data: ContactFormData) -> None:
        """Fill all text fields with provided data."""
        with allure.step('Fill all contact form fields'):
            if data.first_name:
                try:
                    self.name_input.wait_for(state='visible', timeout=5000)
                    self.name_input.fill(data.first_name)
                except:
                    pass  # Field may not exist
                    
            if data.last_name:
                try:
                    self.last_name_input.wait_for(state='visible', timeout=5000)
                    self.last_name_input.fill(data.last_name)
                except:
                    pass
                    
            if data.email:
                try:
                    self.email_input.wait_for(state='visible', timeout=5000)
                    self.email_input.fill(data.email)
                except:
                    pass
                    
            if data.secondary_email:
                try:
                    self.secondary_email_input.wait_for(state='visible', timeout=5000)
                    self.secondary_email_input.fill(data.secondary_email)
                except:
                    pass
                    
            if data.phone:
                try:
                    self.phone_input.wait_for(state='visible', timeout=5000)
                    self.phone_input.fill(data.phone)
                except:
                    pass
                    
            if data.company:
                try:
                    self.company_input.wait_for(state='visible', timeout=5000)
                    self.company_input.fill(data.company)
                except:
                    pass
                    
            if data.job_title:
                try:
                    self.job_title_input.wait_for(state='visible', timeout=5000)
                    self.job_title_input.fill(data.job_title)
                except:
                    pass
                    
            if data.comment:
                try:
                    self.comment_input.wait_for(state='visible', timeout=5000)
                    self.comment_input.fill(data.comment)
                except:
                    pass

    @allure.step
    def set_checkboxes(self, data: ContactFormData) -> None:
        """Set checkboxes based on contact data."""
        with allure.step('Set contact form checkboxes'):
            try:
                if data.is_primary:
                    self.primary_checkbox.check()
                else:
                    self.primary_checkbox.uncheck()
            except:
                pass
                
            try:
                if data.is_emergency:
                    self.emergency_checkbox.check()
                else:
                    self.emergency_checkbox.uncheck()
            except:
                pass
                
            # Optional checkboxes
            if data.is_billing is not None:
                try:
                    if data.is_billing:
                        self.billing_checkbox.check()
                    else:
                        self.billing_checkbox.uncheck()
                except:
                    pass
                    
            if data.is_technical is not None:
                try:
                    if data.is_technical:
                        self.technical_checkbox.check()
                    else:
                        self.technical_checkbox.uncheck()
                except:
                    pass
                    
            if data.is_abuse is not None:
                try:
                    if data.is_abuse:
                        self.abuse_checkbox.check()
                    else:
                        self.abuse_checkbox.uncheck()
                except:
                    pass

    @allure.step
    def fill_form(self, data: ContactFormData) -> None:
        """Fill entire form with provided data."""
        with allure.step('Fill contact form'):
            self.fill_all_fields(data)
            self.set_checkboxes(data)

    @allure.step
    def click_create(self) -> None:
        """Click the Create button."""
        with allure.step('Click Create button'):
            self.create_button.wait_for(state='visible', timeout=10000)
            self.create_button.click()

    @allure.step
    def click_save(self) -> None:
        """Click the Save button."""
        with allure.step('Click Save button'):
            self.save_button.wait_for(state='visible', timeout=10000)
            self.save_button.click()
