
import json
import logging
import requests
from urllib.parse import urljoin


import features.env_utils as env_utils
from features.steps.api.api_utils import raise_http_error
from behave import step


@step(u'I login to demoqa page through API')
def get_access_token(context):
    # preparing data
    app_url = env_utils.get_app_url(context)
    user_name = env_utils.get_testing_user_name(context)
    password = env_utils.get_testing_user_password(context)

    # preparing request
    data = {"userName": user_name, "password": password}
    url = urljoin(app_url, 'Account/v1/GenerateToken')
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # performing HTTP request
    response = requests.post(url, data=json.dumps(data), headers=headers)
    # managing response data
    if response.status_code == 200:
        context.access_token = response.json().get("token")
    else:
        raise_http_error(response)

@step(u'I see the response contains the access token')
def verify_response_contains_access_token(context):
    assert context.access_token is not None, "Access token is not present in the response"
    logging.info("Access token is present in the response")

