Feature: Get a single team

    Scenario: Get a team without competition
        Given I have a team "Manchester United" in "ENG"
        When I call v2/team/MNU
        Then I get an OK response
