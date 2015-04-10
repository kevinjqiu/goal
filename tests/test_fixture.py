from base import BaseTestCase


class TestFixture(BaseTestCase):
    def test_get_all_fixtures(self, cd1_season1, cpl_season1):
        response = self.make_api_request('GET', 'v2/fixtures')
        assert len(response.json()['fixtures']) == (6 + 12)

    def test_get_fixtures_in_season_cd1(self, cd1_season1, cpl_season1):
        response = self.make_api_request('GET', 'v2/fixtures?season_id=99')
        assert len(response.json()['fixtures']) == 6

    def test_get_fixtures_in_season_cpl(self, cd1_season1, cpl_season1):
        response = self.make_api_request('GET', 'v2/fixtures?season_id=66')
        assert len(response.json()['fixtures']) == 12

    def test_get_fixtures_by_game_day(self, cpl_season1):
        response = self.make_api_request(
            'GET', 'v2/fixtures?season_id=66&gameday=1')
        assert len(response.json()['fixtures']) == 2
        response = self.make_api_request(
            'GET', 'v2/fixtures?season_id=66&gameday=2')
        assert len(response.json()['fixtures']) == 2

    def test_get_fixtures_by_non_existent_game_day(self, cpl_season1):
        response = self.make_api_request(
            'GET', 'v2/fixtures?season_id=66&gameday=0')
        assert len(response.json()['fixtures']) == 0
