# Python with Behavex Solution

## Setup

### Pre-requisites
- Install Git: https://github.com/git-guides/install-git
- Install Python 3.8: https://www.python.org/downloads/release/python-380/
  - (the testing solution is not proven yet to work with Python 3.9)
- Install pipenv: https://pypi.org/project/pipenv
- Install the solution:
  - Open a command line in a folder where you want to store the testing solution and clone the python_behavex_project solution
    (You can find the command in github)

### For this example, the following environment variables need to be set: APP_URL, USER_NAME and USER_PASSWORD

The testing user should be already created in https://demoqa.com/ page.
Once you create a testing user, use the user name and password specified to set the variables.


To set the environment variables, there are different options available. Choose one of them:

- Duplicate .env-sample and rename it to .env. Then edit the .env file with your own values.

- Set the environment variables in the .env file:

  - APP_URL=https://demoqa.com/
  - USER_NAME=<testing_user_name>
  - PASSWORD=A<testing_user_password>


### Install testing solution dependencies
From root project folder execute the following command: ```pipenv install```

### To execute tests locally:

There are different ways to execute the tests locally. For both the available browsers are: firefox or chrome.
Remember to download previously the chromedriver or geckodriver files.

- Using the command line: execute the following command, by replacing \<TAG\> by any scenario tags you would like to execute:

  ```
  pipenv run behavex -t <TAG> -D browser=<browser>
  ```

### Running in headless mode
If you need to run locally in headless mode, you need to add the following parameter: -D headless_browser=true

- Executing by the terminal:

  ```
  pipenv run behavex -t <TAG> -D browser=chrome -D headless_browser=true
  ```

- Adding it in the Pycharm configuration as a parameter:

  -t <TAG> -D browser=chrome -D headless_browser=true


### Testing solution documentation
As the testing solution consists of a wrapper (called BehaveX) on top of Python Behave, please take a look at the Behave documentation:
https://behave.readthedocs.io/en/stable/
