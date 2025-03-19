"""
This page object contains the elements locators and methods related to the Login page
"""

import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By

from features.steps.pages.base_page import BasePage


class LoginPage(BasePage):

    user_name_text_field = (By.ID, "userName")
    user_password_text_field = (By.ID, "password")
    login_button = (By.ID, "login")
    loading_message = (By.ID, "loading-label")

    def __init__(self, driver, app_url):
        super().__init__(driver)
        BasePage.app_url = app_url
        self.login_url = urljoin(app_url, "login")

    def open_tools_qa_login_page(self):
        self.driver.get(self.login_url)
        logging.info("Login page opened")

    def complete_user_name_field(self, user_name):
        user_name_field = self.web_utils.find_element(*self.user_name_text_field)
        user_name_field.send_keys(user_name)

    def complete_user_password_field(self, user_password):
        user_password_field = self.web_utils.find_element(*self.user_password_text_field)
        user_password_field.send_keys(user_password)

    def click_login_button(self):
        login_button = self.web_utils.find_element(*self.login_button)

        self.web_utils.safe_click(login_button)
        self.web_utils.wait_element_to_hide(*self.loading_message)
        from features.steps.pages.profile_page import ProfilePage

        return ProfilePage(self.driver)
