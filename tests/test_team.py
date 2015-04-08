import requests
from .base import BaseTestCase
from goal.db import get_engine, Base, Team
from nose.plugins.skip import SkipTest


class TestTeamResource(BaseTestCase):
    def test_get_team_without_competition(self):
        self.create_team(
            team_id='MNU', name='Manchester United',
            country_id='ENG')

        response = self.make_api_request('GET', 'v2/teams/MNU')
        assert response.status_code == 200
        assert response.json(), {
            'teams': [{
                'current_competition_id': None,
                'country_id': 'ENG',
                'id': 'MNU',
                'name': 'Manchester United',
            }]
        }

    def test_get_team_with_competition(self):
        self.create_english_premier_league()
        self.create_team(
            team_id='MNU', name='Manchester United',
            country_id='ENG', current_competition_id='EPL')
        response = self.make_api_request('GET', 'v2/teams/MNU')
        assert response.status_code == 200
        assert response.json(), {
            'teams': [{
                'current_competition_id': 'EPL',
                'country_id': 'ENG',
                'id': 'MNU',
                'name': 'Manchester United',
            }]
        }

    def test_get_team_not_found(self):
        raise SkipTest
        response = self.make_api_request('GET', 'v2/teams/MNU')
        assert response.status_code == 404
