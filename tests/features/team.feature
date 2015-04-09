Feature: Get a single team

    Scenario: Get a team without competition
        Given I have a team "Arsenal"
        When I call GET v2/teams/ARS
        Then I get an OK response
        And The response matches {"teams": [{"id": "ARS", "name": "Arsenal", "country_id": "ENG", "current_competition_id": null}]}
