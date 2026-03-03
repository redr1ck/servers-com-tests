from playwright.sync_api import Page

from src.elements import BaseElement, Button


class Dialog(BaseElement):
    """Represents a generic dialog/modal element that can be used for confirmation dialogs, forms, etc."""

    def __init__(self, page: Page):
        """
        Initialize a Dialog element.

        Args:
            page: The Playwright Page object
        """
        # Use flexible locator to find the dialog container
        container_locator = page.get_by_role("dialog").first
        super().__init__(page, container_locator, "Dialog")
        self.delete_button = Button(self.page, "Delete")

    @property
    def type_of(self) -> str:
        """Gets the lowercase type of the element."""
        return 'dialog'