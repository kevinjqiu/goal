import pytest
from base import BaseTestCase


class TestSeasonGet(BaseTestCase):
    def test_get_non_existent_season(self):
        pytest.skip('Not implemented')
        response = self.make_api_request('GET', 'v2/seasons/99')
        assert 0 == len(response.json()['seasons'])

    def test_get_existing_season(self, cpl_season1):
        response = self.make_api_request('GET', 'v2/seasons/66')
        assert response.json() == {'seasons': [{
            'competition_id': 'CPL',
            'start_year': 2015,
            'num_game_days': 6,
            'end_year': 2015,
            'next_game_day': 1,
            'id': 66}]}
