Feature: Search fixtures

    Scenario: Search all fixtures
        Given I have a team "Toronto"
        And I have a team "Montreal"
        And I have a team "Vancouver"
        When I start a new CPL season
        And I call GET v2/fixtures
        Then I get a response: 200
        And I get 6 fixtures

    Scenario: Search by non-existent season id
        Given I have a team "Toronto"
        And I have a team "Montreal"
        And I have a team "Vancouver"
        When I start a new CPL season
        And I call GET v2/fixtures?season_id=999
        Then I get a response: 200
        And I get 0 fixtures

    Scenario: Search by existing season id
        Given I have a team "Toronto"
        And I have a team "Montreal"
        And I have a team "Vancouver"
        When I start a new CPL season with id: 999
        And I call GET v2/fixtures?season_id=999
        Then I get a response: 200
        And I get 6 fixtures

    # Scenario: Search by game day
    #     Given I have a team "Toronto"
    #     And I have a team "Montreal"
    #     And I have a team "Vancouver"
    #     When I start a new CPL season with id: 999
    #     And I call GET v2/fixtures?season_id=999&game_day=1
    #     Then I get a response: 200
    #     And I get 1 fixtures
