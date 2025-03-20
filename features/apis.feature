# Created by creusserp 03/2025
Feature: Api
  # This feature is going to be used for all the tests related to API testing

  
  Scenario: I can login Tools QA page through the API
    Given I login to demoqa page through API
    Then I see the response contains the access token
