"""
This module contains the definition of steps used by the BDD tests related to the Login page
"""

from behave import step

from features.env_utils import get_testing_user_name, get_testing_user_password
from features.steps.pages.login_page import LoginPage as LP


@step("I complete the user name field with testing user name")
def complete_user_name_field(context):
    """ Step to complete user name field with the name provided by the env variable user_name"""
    user_email = get_testing_user_name(context)
    login_page: LP = context.current_page
    login_page.complete_user_name_field(user_email)


@step("I complete the password field with testing user password")
def complete_password_field(context):
    """ Step to complete user password field with the name provided by the env variable user_password """
    user_password = get_testing_user_password(context)
    login_page: LP = context.current_page
    login_page.complete_user_password_field(user_password)


@step("I click the Login button")
def click_button_by_text(context):
    """ Step to click login button to perform the login action """
    login_page: LP = context.current_page
    context.current_page = login_page.click_login_button()
