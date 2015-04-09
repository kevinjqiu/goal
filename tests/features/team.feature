Feature: Get a single team

    Scenario: Get a team without current competition
        Given I have a team "Arsenal"
        When I call GET v2/teams/ARS
        Then I get a response: 200
        And The response matches {"teams": [{"id": "ARS", "name": "Arsenal", "country_id": "ENG", "current_competition_id": null}]}

    Scenario: Get a team with current competition
        Given I have a team "Man Utd" in EPL
        When I call GET v2/teams/MNU
        Then I get a response: 200
        And The response matches {"teams": [{"id": "MNU", "name": "Man Utd", "country_id": "ENG", "current_competition_id": "EPL"}]}
