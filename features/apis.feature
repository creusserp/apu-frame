# Created by pcreusser 03/2025
Feature: Api
  # This feature is going to be used for all the tests related to login and creation of new accounts

  @RUN
  Scenario: I can login Tools QA page through the API
    Given I login to demoqa page through API
    Then I see the response contains the access token
