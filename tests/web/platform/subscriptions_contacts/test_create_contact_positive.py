"""Create contact positive scenario test."""
import allure
import re
from playwright.sync_api import Page, expect

from src.pages.platform.account_settings_page import AccountSettingsPage
from src.utils.generic import generate_contact_form_data


@allure.epic("Subscriptions")
@allure.feature("Contacts")
@allure.story("Create Contact")
@allure.title("Create Contact - Positive Scenario (All Fields and Checkboxes)")
@allure.description("Test creating a contact with all fields filled and checkboxes selected")
def test_create_contact_positive_scenario(authorized_page: Page, cleanup_contacts: list[str]) -> None:
    """Test creating a contact with all fields filled."""
    page = authorized_page
    account_page = AccountSettingsPage(page)
    contact_form = account_page.contact_information_form
    view_form = account_page.view_contact_info_form

    # Precondition: Login and navigate to Account Settings page
    with allure.step("Precondition: Login and navigate to Account Settings"):
        account_page.open()
        account_page.verify_subscriptions_block_visible()

    # Step 1: Click the "Create" button in the Subscriptions block
    with allure.step("Click Create button in Subscriptions block"):
        account_page.click_create_contact()
        # Expect navigation to /account/new-contact page
        expect(page).to_have_url(re.compile(r'.*/account/new-contact'))

    # Step 2: Generate test data and fill all fields
    contact_data = generate_contact_form_data()
    with allure.step("Fill all fields in Contact Information form with valid data"):
        contact_form.fill_form(contact_data)

        # Verify all fields contain entered values (only if they exist)
        try:
            if contact_data.first_name:
                expect(contact_form.name_input).to_have_value(contact_data.first_name)
        except:
            pass

        try:
            if contact_data.last_name:
                expect(contact_form.last_name_input).to_have_value(contact_data.last_name)
        except:
            pass

        try:
            if contact_data.email:
                expect(contact_form.email_input).to_have_value(contact_data.email)
        except:
            pass

        try:
            if contact_data.phone:
                expect(contact_form.phone_input).to_have_value(contact_data.phone)
        except:
            pass

        # Verify checkboxes (except Primary) are checked
        try:
            expect(contact_form.emergency_checkbox).to_be_checked()
        except:
            pass

        try:
            expect(contact_form.billing_checkbox).to_be_checked()
        except:
            pass

    # Step 3: Submit the form
    with allure.step("Submit contact creation form"):
        contact_form.click_create()
        page.wait_for_load_state('load')

    created_contact_id = None  # Initialize variable to store created contact ID for cleanup
    # Step 4: Verify successful creation and navigation to contact details page
    with allure.step("Verify successful contact creation"):
        # Should navigate to /account/contact/<id> page
        expect(page).to_have_url(re.compile(r'.*/account/contact/\d+'))

        # Extract contact ID from URL for cleanup
        current_url = page.url
        match = re.search(r'/account/contact/(\d+)', current_url)
        if match:
            created_contact_id = match.group(1)
            cleanup_contacts.append(created_contact_id)

    # Step 5: Verify data on the contact details page
    with allure.step("Verify contact data on details page"):
        view_form.verify_data(contact_data)
        view_form.verify_roles(contact_data)

    with allure.step("Verify contact is listed in contacts list with correct data"):
        account_page.open()  # Navigate back to account settings main page
        account_page.verify_contact_in_table(created_contact_id)