"""
This file is used to store all the common methods related to the env configuration
"""


def get_app_url(context):
    app_url = context.env_config["app_url"]
    return app_url


def get_testing_user_name(context):
    user_name = context.env_config["user_name"]
    return user_name


def get_testing_user_password(context):
    user_password = context.env_config["user_password"]
    return user_password
