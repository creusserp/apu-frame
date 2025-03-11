
import logging
import os

from behavex_images import extend_environment as bxi_env
from behaving.web import environment as bng_env
from selenium import webdriver
from dotenv import load_dotenv


load_dotenv()

def before_all(context):
    if all(
        env_var in os.environ for env_var in ["APP_URL", "USER_NAME", "PASSWORD"]
    ):
        app_url = os.getenv("APP_URL")
        user_name = os.getenv("USER_NAME")
        user_password = os.getenv("PASSWORD")
        context.env_config = {
            "app_url": app_url,
            "user_name": user_name,
            "user_password": user_password,
        }
        
    else:
        raise Exception(
            "The following environment variables are required to execute the tests: "
            "APP_URL, USER_NAME and USER_PASSWORD"
        )
    context.execution_summary_filename = os.path.abspath(
        os.path.join(os.environ.get("OUTPUT"), "execution_summary.txt")
    )
    if 'BROWSER' in os.environ:
        context.selected_browser = os.environ.get('BROWSER').lower()
    else:
        context.selected_browser = context.config.userdata.get('browser', 'chrome')
    if context.selected_browser in ('firefox', 'chrome'):
        context.default_browser = context.selected_browser
        logging.info("Selected browser: {}".format(context.selected_browser))
    else:
        logging.info(
            '\n-----------------------------\n'
            '{} is not a valid option for executions in local browsers\n'
            '-----------------------------'.format(context.selected_browser)
        )
        exit()
    bng_env.before_all(context)
    bxi_env.before_all(context)

    # Setting default logging level for selenium for web based tests
    logger_name = 'selenium.webdriver.remote.remote_connection'
    selenium_logger = logging.getLogger(logger_name)
    selenium_logger.propagate = False
    selenium_logger.setLevel(logging.WARNING)

def before_feature(context, feature):
    bng_env.before_feature(context, feature)
    bxi_env.before_feature(context, feature)


def before_scenario(context, scenario):
    bng_env.before_scenario(context, scenario)
    bxi_env.before_scenario(context, scenario)
    if "selected_browser" in context:
        if context.config.userdata.get("headless_browser", None):
            run_browser_headless_mode(context)
        else:
            run_browser_non_headless_mode(context)
            if ("options" in context.browser_args
                    and "--headless" in context.browser_args["options"].arguments):
                context.browser_args["options"].arguments.remove("--headless")
    print("-" * 40)
    print("Running Scenario: {}".format(scenario.name))
    print("-" * 40)

def before_step(context, step):
    bxi_env.before_step(context, step)
    """before_step behave hook"""
    logging.info("-" * 40)
    logging.info("STEP: {}".format(step.name))
    context.step = step

def after_step(context, step):
    bxi_env.after_step(context, step)

def after_scenario(context, scenario):
    with open(context.execution_summary_filename, "a+") as f:
        scenario_status = str(scenario.status).split(".")[-1]
        if ("MUTE" in scenario.tags
            and "MANUAL" not in scenario.tags
                and "WIP" not in scenario.tags):
            # This is automated scenario that has been MUTED
            f.write("MUTED_SCENARIO: {}: {}\n".format(scenario.feature.name, scenario.name))
        if "MUTE" not in scenario.tags and "failed" in scenario_status:
            f.write("FAILING_SCENARIO: {}: {}\n".format(scenario.feature.name, scenario.name))
        if scenario_status in ["passed", "failed"]:
            f.write("EXECUTED_SCENARIO: {}: {}\n".format(scenario.feature.name, scenario.name))
            print("------------------------------------------")
            print("Scenario Completed (Status: {}): {}".format(scenario_status.upper(), scenario.name))
            print("------------------------------------------")
    bxi_env.after_scenario(context, scenario)
    if (scenario.status in ('failed', 'untested')
            and 'AUTORETRY' in scenario.tags and os.environ.get('AUTORETRY_ATTEMPT', None) == '0'):
        bng_env.teardown(context)
    else:
        bng_env.after_scenario(context, scenario)


def after_feature(context, feature):
    bng_env.after_feature(context, feature)
    bxi_env.after_feature(context, feature)


def after_all(context):
    bxi_env.after_all(context)
    if 'browsers' in context:
        bng_env.after_all(context)

# ####################################################################################################
# ########################################## HELPER METHODS ##########################################
# ####################################################################################################


def run_browser_headless_mode(context):
    if "options" in context.browser_args:
        options = context.browser_args["options"]
    else:
        options = set_browser_options(context.default_browser)
    options.add_argument("--headless")
    context.browser_args["options"] = options


def run_browser_non_headless_mode(context):
    if "options" in context.browser_args:
        options = context.browser_args["options"]
    else:
        options = set_browser_options(context.default_browser)
    context.browser_args["options"] = options


def set_browser_options(browser):
    if 'chrome' in browser:
        options = webdriver.ChromeOptions()
    elif 'firefox' in browser:
        options = webdriver.FirefoxOptions()
    else:
        raise Exception("Default browser is not valid. Valid options: Chrome or Firefox")
    return options
