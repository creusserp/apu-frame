"""
This page object contains the elements locators and methods related to the text-box page
"""

from urllib.parse import urljoin
from playwright.sync_api import Page

from features.steps.pages.base_page import BasePage


class TextboxPage(BasePage):

    page_label = "//h1[contains(text(),'Text Box')]"  # XPath for the page label

    def __init__(self, page: Page):
        super().__init__(Page)
    
    def get_page_title(self):
        """Retrieve the page title."""
        page_title = self.page.locator(self.page_label).text_content()
        return page_title
