"""
This page object contains the elements locators and methods related to the text-box page
"""

import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By

from features.steps.pages.base_page import BasePage


class TextboxPage(BasePage):

    page_label = (By.XPATH, "//h1[contains(text(),'Text Box')]")

    def __init__(self, driver):
        super().__init__(driver)
    
    def get_page_title(self):
        page_title = self.web_utils.find_element(*self.page_label).text
        return page_title
