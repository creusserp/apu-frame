"""
This page object contains the elements locators and methods related to the Login page
"""

import logging
from urllib.parse import urljoin
from features.steps.pages.base_page import BasePage

from playwright.sync_api import Page


class LoginPage(BasePage):
    
    user_name_text_field = "#userName"  # CSS selector for the username field
    user_password_text_field = "#password"  # CSS selector for the password field
    login_button = "#login"  # CSS selector for the login button
    loading_message = "#loading-label"  # CSS selector for the loading message


    def __init__(self, page: Page, app_url):
        super().__init__(page)
        self.page = page
        BasePage.app_url = app_url
        self.login_url = urljoin(app_url, "login")

    def open_tools_qa_login_page(self):
        """Navigate to the login page."""
        self.page.goto(self.login_url)
        logging.info("Login page opened")

    def complete_user_name_field(self, user_name):
        """Fill the username field."""
        self.page.fill(self.user_name_text_field, user_name)

    def complete_user_password_field(self, user_password):
        """Fill the password field."""
        self.page.fill(self.user_password_text_field, user_password)

    def click_login_button(self):
        """Click the login button and wait for the loading message to disappear."""
        self.page.click(self.login_button)
        self.page.wait_for_selector(self.loading_message, state="hidden")
        logging.info("Login page opened")
        from features.steps.pages.profile_page import ProfilePage

        return ProfilePage(self.page)
        
    
