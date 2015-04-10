from base import BaseTestCase


class TestTeam(BaseTestCase):
    def test_get_team(self, toronto, montreal):
        response = self.make_api_request('GET', 'v2/teams/TOR')
        assert response.json(), {
            'teams': [{
                'current_competition_id': 'CPL',
                'country_id': 'CAN',
                'id': 'TOR',
                'name': 'Toronto FC'}]}
