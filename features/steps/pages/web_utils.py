# -*- coding: utf-8 -*-
"""
This module contains functions for performing
basic web related actions using Selenium WebDriver
Class:
    - WebUtils
        Properties;
           - driver
           - url
       Methods:
           - get
           - find_element
           - find_elements
           - find_element_by_id
           - find_elements_by_id
           - find_element_by_name
           - find_elements_by_name
           - find_element_by_xpath
           - find_elements_by_xpath
           - find_element_by_css_selector
           - find_elements_by_css_selector
           - find_element_by_class_name
           - find_elements_by_class_name
           - find_element_by_partial_link_text
           - find_element_by_link_text
           - wait_element_to_hide
           - wait_for_element_to_be_clickable
           - move_to
           - mouse_hover
           - highlight
"""
# pylint: disable=W0703
import logging
import time

import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as exp_cond


class WebUtils(object):
    """Class containing core functions for interacting with web pages"""
    javascript_click = "arguments[0].click();"

    url = None
    highlight_elements = False

    def __init__(self, driver):
        self.driver = driver
        self.highlight_elements = True

    def get(self, url):
        """Go to the specified url"""
        self.driver.get(url)

    # pylint: disable=R0913
    def find_element(self, by_locator, locator, wait=1, retries=10, wait_for_clickable=True, log_errors=True,):
        """Retrieves the first element found in driver's current page
        based on a specified locator, considering retry intervals
        to properly deal with page loading times"""
        element = None
        if by_locator == By.LINK_TEXT:
            element = self.find_element_by_link_text(locator, wait, retries, log_errors)
        elif by_locator == By.ID:
            element = self.find_element_by_id(locator, wait, retries, wait_for_clickable, log_errors)
        elif by_locator == By.NAME:
            element = self.find_element_by_name(locator, wait, retries, wait_for_clickable, log_errors)
        elif by_locator == By.XPATH:
            element = self.find_element_by_xpath(locator, wait, retries, wait_for_clickable, log_errors)
        elif by_locator == By.CLASS_NAME:
            element = self.find_element_by_class_name(locator, wait, retries, wait_for_clickable, log_errors)
        elif by_locator == By.PARTIAL_LINK_TEXT:
            element = self.find_element_by_partial_link_text(locator, wait, retries, log_errors)
        elif by_locator == By.CSS_SELECTOR:
            locator = locator.replace('"', "'").replace("'", "'").replace("\\'", "'")
            element = self.find_element_by_css_selector(locator, wait, retries, wait_for_clickable, log_errors)
        else:
            for i in range(retries):
                try:
                    element = self.driver.find_element(by_locator, locator, log_errors)
                    break
                except Exception as exception:
                    message = ("Unable to find element with {}: '{}'."
                               "Retry number: {} out of {}.".format(by_locator, locator, str(i + 1),
                                                                    str(retries)))
                    if (i + 1) == retries:
                        raise exception
                    elif log_errors:
                        logging.info(message)
        return element

    def find_elements(self, by_locator, locator, wait=1, retries=8, log_errors=True):
        """Retrieves a list of all elements found in driver's current page
        based on a specified locator, considering retry intervals
        to properly deal with page loading times"""
        elements = None
        if by_locator == By.ID:
            elements = self.find_elements_by_id(locator, wait, retries, log_errors)
        elif by_locator == By.NAME:
            elements = self.find_elements_by_name(locator, wait, retries, log_errors)
        elif by_locator == By.XPATH:
            elements = self.find_elements_by_xpath(locator, wait, retries, log_errors)
        elif by_locator == By.CLASS_NAME:
            elements = self.find_elements_by_class_name(locator, wait, retries, log_errors)
        elif by_locator == By.CSS_SELECTOR:
            locator = locator.replace('"', "'").replace("'", "'").replace("\\'", "'")
            elements = self.find_elements_by_css_selector(locator, wait, retries, log_errors)
        else:
            for i in range(retries):
                try:
                    elements = self.driver.find_elements(by_locator, locator)
                    break
                except Exception as exception:
                    message = ("Unable to find element with {}: '{}'."
                               "Retry number: {} out of {}.".format(by_locator, locator,
                                                                    str(i + 1), str(retries)))
                    if (i + 1) == retries:
                        raise exception
                    elif log_errors:
                        logging.info(message)
        return elements

    def find_element_by_id(self, element_id, wait=2, retries=8, wait_for_clickable=True, log_errors=True):
        """Retrieves a web element using the ID locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    # so it could still exist but if it isn't enabled- won't
                    # show :-/
                    elem = wd_wait.until(exp_cond.element_to_be_clickable((By.ID, element_id)))
                else:
                    elem = wd_wait.until(exp_cond.presence_of_element_located((By.ID, element_id)))
                    elem = self.driver.find_element(By.ID, element_id)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = ("Unable to find element with id: '{}'. "
                           "Retry number: {} out of {}.".format(element_id, str(i + 1), str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_id(self, element_id, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the ID locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(exp_cond.presence_of_all_elements_located((By.ID, element_id)))
                break
            except Exception as exception:
                message = ("Unable to find elements with id: '{}'."
                           "Retry number: {} out of {}.".format(element_id, str(i + 1), str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_name(self, name, wait=1, retries=8, wait_for_clickable=True, log_errors=True):
        """Retrieves a web element using the NAME locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    # so it could still exist but if it isn't enabled- won't
                    # show :-/
                    elem = wd_wait.until(exp_cond.element_to_be_clickable((By.NAME, name)))
                else:
                    elem = wd_wait.until(exp_cond.presence_of_element_located((By.NAME, name)))
                    elem = self.driver.find_element(By.NAME, name)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = ("Unable to find element with name: '{}'."
                           "Retry number: {} out of {}.".format(name, str(i + 1), str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_name(self, name, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the NAME locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(exp_cond.presence_of_all_elements_located((By.NAME, name)))
                break
            except Exception as exception:
                message = ("Unable to find elements with name: '{}'."
                           "Retry number: {} out of {}.".format(name, str(i + 1), str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_xpath(self, xpath, wait=10, retries=8, wait_for_clickable=True, log_errors=True):
        """Retrieves a web element using the XPATH locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    # so it could still exist but if it isn't enabled- won't
                    # show :-/
                    elem = wd_wait.until(exp_cond.element_to_be_clickable((By.XPATH, xpath)))
                else:
                    elem = wd_wait.until(exp_cond.presence_of_element_located((By.XPATH, xpath)))
                    elem = self.driver.find_element(By.XPATH, xpath)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = ("Unable to find element with xpath: '{}'. "
                           "Retry number: {} out of {}.".format(xpath.encode("utf8"), str(i + 1), str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_xpath(self, xpath, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the XPATH locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(exp_cond.presence_of_all_elements_located((By.XPATH, xpath)))
                break
            except Exception as exception:
                message = ("Unable to find element with xpath: '{}'."
                           "Retry number: {} out of {}.".format(xpath.encode("utf8"), str(i + 1), str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_css_selector(self, css, wait=1, retries=8, wait_for_clickable=True, log_errors=True):
        """Retrieves a web element using the CSS selector locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    # so it could still exist but if it isn't enabled- won't
                    # show :-/
                    elem = wd_wait.until(exp_cond.element_to_be_clickable((By.CSS_SELECTOR, css)))
                else:
                    elem = wd_wait.until(exp_cond.presence_of_element_located((By.CSS_SELECTOR, css)))
                    elem = self.driver.find_element(By.CSS_SELECTOR, css)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = ("Unable to find element with css selector: '{}'."
                           "Retry number: {} out of {}.".format(css.encode("utf8"), str(i + 1), str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_css_selector(self, css, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the CSS SELECTOR locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(exp_cond.presence_of_all_elements_located((By.CSS_SELECTOR, css)))
                break
            except Exception as exception:
                message = ("Unable to find element with css selector: '{}'."
                           "Retry number: {} out of {}.".format(css.encode("utf8"), str(i + 1), str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_class_name(self, class_name, wait=1, retries=8, wait_for_clickable=True, log_errors=True):
        """Retrieves a web element using the CLASS NAME locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    # so it could still exist but if it isn't enabled- won't
                    # show :-/
                    elem = wd_wait.until(exp_cond.element_to_be_clickable((By.CLASS_NAME, class_name)))
                else:
                    elem = wd_wait.until(exp_cond.presence_of_element_located((By.CLASS_NAME, class_name)))
                    elem = self.driver.find_element(By.CLASS_NAME, class_name)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = ("Unable to find element with class name: '{}'."
                           "Retry number: {} out of {}.".format(class_name.encode("utf8"),
                                                                str(i + 1),
                                                                str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_class_name(self, class_name, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the CLASS NAME locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(exp_cond.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
                break
            except Exception as exception:
                message = ("Unable to find element with css selector: '{}'."
                           "Retry number: {} out of {}.".format(class_name.encode("utf8"),
                                                                str(i + 1),
                                                                str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_partial_link_text(self, partial_link_text, wait=1, retries=8, log_errors=True):
        """Retrieves a web element using the CLASS NAME locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elem = wd_wait.until(
                    exp_cond.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, partial_link_text))
                    and exp_cond.visibility_of_element_located((By.PARTIAL_LINK_TEXT, partial_link_text))
                    and exp_cond.element_to_be_clickable((By.PARTIAL_LINK_TEXT, partial_link_text)))
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = ("Unable to find element with partial link text containing: '{}'."
                           "Retry number: {} out of {}.".format(partial_link_text.encode("utf8"), str(i + 1),
                                                                str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_element_by_link_text(self, text, wait=1, retries=8, log_errors=True):
        """Retrieves a web element using the LINK TEXT locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if i % 2 == 0:
                    elem = wd_wait.until(exp_cond.element_to_be_clickable((By.LINK_TEXT, text)))
                else:
                    elem = wd_wait.until(exp_cond.element_to_be_clickable((By.XPATH, "//a[text()='" + text + "']")))
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = ("Unable to find element with link text: '{}'. "
                           "Retry number: {} out of {}.".format(text, str(i + 1), str(retries)))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def wait_element_to_hide(self, by_locator, locator, wait=1, retries=8):
        for i in range(retries):
            # noinspection PyBroadException
            try:
                self.driver.find_element(by_locator, locator)
                time.sleep(wait)
            except:
                return
        raise Exception("Element is still visible: {}:{}".format(by_locator, locator))

    def wait_for_element_to_be_clickable(self, by_locator, locator, wait=3, retries=3):
        for i in range(retries):
            # noinspection PyBroadException
            try:
                ui.WebDriverWait(self.driver, wait).until(exp_cond.element_to_be_clickable((by_locator, locator)))
            except:
                return
        raise Exception("Element is not clickable: {}:{}".format(by_locator, locator))

    def move_to(self, element, x_offset=0, y_offset=0, show_element_at_top=True):
        show_at_top = "true" if show_element_at_top else "false"
        self.driver.execute_script("arguments[0].scrollIntoView({});".format(show_at_top), element)
        self.mouse_hover(element, x_offset, y_offset)

    def mouse_hover(self, element, x_offset=0, y_offset=0):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).move_by_offset(x_offset, y_offset).perform()

    def safe_click(self, element, javascript_only=False):
        """
        Performs a click on a web element in a robust manner.
        This method first attempts a normal click on the element. If an ElementClickInterceptedException is raised,
        it tries to click on the element using JavaScript.
        Args:
            element: selenium webelement.
        """
        if javascript_only:
            try:
                # Attempt a javascript click
                self.driver.execute_script(self.javascript_click, element)
            except Exception as ex:
                logging.error(f"Failed to click on element: {element}. Error: {ex}")
                raise ex
        else:
            try:
                # Attempt a normal click
                element.click()
            except Exception:
                # If the click is intercepted, try using JavaScript
                try:
                    self.driver.execute_script(self.javascript_click, element)
                except Exception as inner_ex:
                    logging.error(f"Failed to click on element: {element}. Error: {inner_ex}")
                    raise inner_ex



def highlight(element, color="blue", border=3):
    """Highlights (blinks) a Selenium Webdriver element"""
    # noinspection PyProtectedMember
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)

        apply_style("border: {0}px solid {1};".format(border, color))

    