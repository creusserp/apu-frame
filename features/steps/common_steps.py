"""
This module contains the definition of common steps used by the BDD tests in the project
"""

import logging

from behave import step
from behaving.web.steps import *

from features.env_utils import get_app_url
from features.steps.pages.login_page import LoginPage
from features.steps.pages.profile_page import ProfilePage as PP
from features.steps.pages.text_box_page import TextboxPage as TB



@step(u'I open the Tools QA page')
def open_main_page(context):
    """Initializes the browser and opens the Tools QA Login page"""
    app_url = get_app_url(context)
    context.execute_steps(
        """
            Given browser "{}"
            And I set browser size to 1400x900
        """.format(
            context.default_browser))
    login_page = LoginPage(context.browser.driver, app_url)
    login_page.open_tools_qa_login_page()
    context.current_page = login_page


@step(u'I set browser size to {size}')
def set_browser_window_size(context, size):
    """Set browser to the specified screen resolution"""
    split_size = size.split('x')
    for browser_selected in context.browsers.values():
        browser_selected.driver.set_window_size(split_size[0], split_size[1])
        logging.info('Browser size has been changed to {0}x{1}'.format(split_size[0], split_size[1]))

@step(u'I expand "{element}" menu')
def expand_menu_panel(context, element):
    """Expand the menu panel"""
    if element == 'Elements':
        context.current_page.expand_panel_menu(element)

@step(u'I click "{option}" option')
def expand_menu_panel_option(context, option):
    """Expand the menu panel"""
    if option == 'Text Box':
        context.current_page.click_panel_menu_option(option)

@step(u'I see the "{page}" page is displayed')
def verify_profile_page_is_displayed(context,page):
    """ Step to verify if url displayed is the profile one"""
    if page == 'profile':
        profile_page: PP = context.current_page
        current_url = profile_page.get_current_url()
        assert ("profile" in current_url), "Current url is not the profile url. Current url: {}".format(current_url)
        logging.info("Current url is the profile url")
    elif page == 'Text Box':
        profile_page: TB = context.current_page
        current_url = profile_page.get_current_url()
        assert ("text-box" in current_url), "Current url is not the text-box url. Current url: {}".format(current_url)
        logging.info("Current url is the text-box url")




   
