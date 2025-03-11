# Created by pcreusser 03/2025
Feature: Login
  # This feature is going to be used for all the tests related to login and creation of new accounts

  @RUN
  Scenario: I can login into the Tools QA page with an existing user and correct password
    Given I open the Tools QA page
    When I complete the user name field with testing user name
    And I complete the password field with testing user password
    And I click the Login button
    Then I see the "profile" page is displayed
    And I see the user name is displayed in the page


  @RUN
  Scenario: After login I can see the "Elements" menu and click on "Text Box" option
    Given I open the Tools QA page
    When I complete the user name field with testing user name
    And I complete the password field with testing user password
    And I click the Login button
    And I expand "Elements" menu
    And I click "Text Box" option
    Then I see the "Text Box" page is displayed
  