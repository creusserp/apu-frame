"""
This page object contains the elements locators and methods related to the Profile page
"""

from playwright.sync_api import Page
from features.steps.pages.base_page import BasePage


class ProfilePage(BasePage):

    user_name_label = "#userName-value" # CSS selector for the username label

    def __init__(self, page: Page):
        super().__init__(page)

    def get_user_name_displayed(self):
        """Retrieve the username displayed on the profile page."""
        user_name_displayed = self.page.locator(self.user_name_label).text_content()
        return user_name_displayed
