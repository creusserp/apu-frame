"""
Base Page Class for Page Object Model (POM)

It encapsulates common functionality and utilities used across multiple pages in the application.
The other page object classes should inherit from this class.

"""

from features.steps.pages.web_utils import WebUtils
from selenium.webdriver.common.by import By


class BasePage:
    app_url = None

    menu_text = (By.XPATH, "//div[contains(text(),'Elements')]")
    menu_option_text = (By.XPATH, "//span[contains(text(),'Text Box')]")
  

    def __init__(self, driver):
        self.driver = driver
        self.web_utils = WebUtils(driver)

    def get_current_url(self):
        return self.driver.current_url
    
    def expand_panel_menu(self, menu):
        if BasePage.app_url:
            if menu == "Elements":
                menu_element = self.web_utils.find_element(*self.menu_text)
                self.web_utils.safe_click(menu_element)

    def click_panel_menu_option(self, option):
        if BasePage.app_url:
            if option  == "Text Box":
                option_element = self.web_utils.find_element(*self.menu_option_text)
                self.web_utils.safe_click(option_element)
                from features.steps.pages.text_box_page import TextboxPage
                return TextboxPage(self.driver)
            
