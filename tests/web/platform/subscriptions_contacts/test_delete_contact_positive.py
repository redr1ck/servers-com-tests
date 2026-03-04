"""Delete contact positive scenario test."""
import allure
from playwright.sync_api import Page

from src.elements.dialog import Dialog
from src.pages.platform.account_settings_page import AccountSettingsPage


@allure.epic("Subscriptions")
@allure.feature("Contacts")
@allure.story("Delete Contact")
@allure.title("Delete Contact - Positive Scenario")
@allure.description("Test deleting an existing contact from the subscriptions table")
def test_delete_contact_positive_scenario(authorized_page: Page, create_contact: str) -> None:
    """Test deleting an existing contact."""
    account_page = AccountSettingsPage(authorized_page)
    confirmation_dialog = Dialog(authorized_page)
    contact_id = str(create_contact)

    # Step 1: Locate the pre-created contact in the Subscriptions table
    with allure.step("Navigate to Account Settings and locate contact in table"):
        account_page.open()
        account_page.verify_subscriptions_block_visible()
        account_page.verify_contact_in_table(contact_id)

    # Step 2: Click the Delete button in the same row
    with allure.step("Click Delete button for the contact"):

        delete_button = account_page.get_delete_button_for_contact(contact_id)
        delete_button.click()

    # Step 3: Click "Delete" in the confirmation dialog
    with allure.step("Confirm deletion by clicking Delete in confirmation dialog"):
        confirmation_dialog.element_locator.wait_for(state='visible')
        confirmation_dialog.delete_button.click()
    
    # Step 4: Verify the contact no longer appears in the Subscriptions table
    with allure.step("Verify contact is removed from Subscriptions table"):
        account_page.verify_contact_not_in_table(contact_id)
