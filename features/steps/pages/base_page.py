"""
Base Page Class for Page Object Model (POM)

It encapsulates common functionality and utilities used across multiple pages in the application.
The other page object classes should inherit from this class.

"""

from playwright.sync_api import Page


class BasePage:
    app_url = None

    menu_text = "//div[contains(text(),'Elements')]"  # XPath for the "Elements" menu
    menu_option_text = "//span[contains(text(),'Text Box')]"  # XPath for the "Text Box" option


    def __init__(self, page: Page):
        self.page = page

    def get_current_url(self):
        """Return the current URL."""
        return self.page.url
    
    def expand_panel_menu(self, menu):
        """Expand the specified menu panel."""
        if BasePage.app_url:
            if menu == "Elements":
                menu_element = self.page.locator(self.menu_text)
                menu_element.click()  # Click the menu element

    def click_panel_menu_option(self, option):
        """Click the specified menu option."""
        if BasePage.app_url:
            # NOTE: This if statement currently handles only the "Text Box" option.
            #Additional options can be added here in the future as needed.
            if option == "Text Box":
                option_element = self.page.locator(self.menu_option_text)
                option_element.click()  # Click the menu option
                from features.steps.pages.text_box_page import TextboxPage
                return TextboxPage(self.page)