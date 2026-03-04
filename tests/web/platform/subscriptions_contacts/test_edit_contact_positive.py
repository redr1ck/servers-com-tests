"""Edit contact positive scenario test."""
import allure
import re
from playwright.sync_api import Page, expect

from src.pages.platform.account_settings_page import AccountSettingsPage
from src.utils.generic import generate_contact_form_data
from src.models.contac_form import ContactFormData


@allure.epic("Subscriptions")
@allure.feature("Contacts")
@allure.story("Edit Contact")
@allure.title("Edit Contact - Positive Scenario (Update All Fields)")
@allure.description("Test editing an existing contact with new data in all fields")
def test_edit_contact_positive_scenario(
    authorized_page: Page,
    create_contact_and_cleanup: tuple[str, ContactFormData],
) -> None:
    """Test editing an existing contact with new data."""
    page = authorized_page
    contact_id, _ = create_contact_and_cleanup
    account_page = AccountSettingsPage(page)
    contact_form = account_page.contact_information_form
    view_form = account_page.view_contact_info_form
    
    # Precondition: Login and navigate to Account Settings page
    with allure.step("Precondition: Login and navigate to Account Settings"):
        account_page.open()
        account_page.verify_subscriptions_block_visible()
        
    with allure.step("Precondition: Find existing contact in Subscriptions table"):
        # Look for any existing contact in the table
        account_page.click_contact(str(contact_id))
         # This will raise an exception if contact not found, which is fine for precondition
    
    # Step 1: Prepare new random valid data for all fields
    updated_data = generate_contact_form_data()
    updated_data.is_abuse = False
    updated_data.is_emergency = False
    updated_data.is_billing = False
    
    with allure.step("Generate new test data for update"):
        # Data is generated and stored in updated_data
        pass
    
    # Step 2: Fill all fields with the new data
    with allure.step("Fill all fields with new data using ContactInformationForm"):
        account_page.view_contact_info_form.click_edit()
        contact_form.fill_all_fields(updated_data)
        
        # Check only the "Emergency" checkbox
        # Primary is disabled and cannot be interacted with
        contact_form.set_checkboxes(updated_data)
        
        # Verify all fields contain new values (skip company as it's not editable)
        if updated_data.first_name:
            expect(contact_form.name_input).to_have_value(updated_data.first_name)
        
        if updated_data.last_name:
            expect(contact_form.last_name_input).to_have_value(updated_data.last_name)
        
        if updated_data.email:
            expect(contact_form.email_input).to_have_value(updated_data.email)
        
        if updated_data.secondary_email:
            expect(contact_form.secondary_email_input).to_have_value(updated_data.secondary_email)
        
        if updated_data.phone:
            expect(contact_form.phone_input).to_have_value(updated_data.phone)
        
        if updated_data.job_title:
            expect(contact_form.job_title_input).to_have_value(updated_data.job_title)
        
        if updated_data.comment:
            expect(contact_form.comment_input).to_have_value(updated_data.comment)
        
        # Verify only Emergency checkbox is checked (Primary state unchanged)
        expect(contact_form.technical_checkbox).to_be_checked()
    
    # Step 3: Submit the form (click Save/Update button)
    with allure.step("Submit the form by clicking Save button"):
        contact_form.click_save()
        # Expect navigation to /account/contact/<contactId> page
        page.wait_for_url(re.compile(r".*/account/contact/\d+"))

    # Step 4: Verify the updated data is saved correctly
    with allure.step("Verify updated data is saved correctly in View form"):
        view_form.should_be_visible()
        view_form.verify_data(updated_data)
        view_form.verify_roles(updated_data)
    
    # Step 5: Navigate back to Account Settings page
    with allure.step("Navigate back to Account Settings page"):
        account_page.open()
        account_page.verify_subscriptions_block_visible()
    
    # Step 6: Verify the updated contact displays correctly in the Subscriptions table
    with allure.step("Verify updated contact displays correctly in Subscriptions table"):
        account_page.verify_contact_in_table(str(contact_id))
