Feature: Get a single team

    Scenario: Get a team without current competition
        Given I have a team "Toronto"
        When I call GET v2/teams/TOR
        Then I get a response: 200
        And The response matches {"teams": [{"id": "TOR", "name": "Toronto FC", "country_id": "CAN", "current_competition_id": "CPL"}]}
