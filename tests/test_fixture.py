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
        for i in xrange(6):
            response = self.make_api_request(
                'GET', 'v2/fixtures?season_id=66&gameday=%d' % (i + 1))
            assert len(response.json()['fixtures']) == 2

    def test_get_fixtures_by_non_existent_game_day(self, cpl_season1):
        response = self.make_api_request(
            'GET', 'v2/fixtures?season_id=66&gameday=0')
        assert len(response.json()['fixtures']) == 0

    def test_get_fixtures_single_fixture_in_game_day(self, cd1_season1):
        response = self.make_api_request(
            'GET', 'v2/fixtures?season_id=99&gameday=1')
        assert len(response.json()['fixtures']) == 1
        assert response.json() == {'fixtures': [{
            'away_score': None,
            'away_team': 'EDM',
            'game_day': 1,
            'home_score': None,
            'home_team': 'HAL',
            'id': 1,
            'links': {
                'away_recent_games': u'/v2/fixtures?team_ids=EDM&count=5&order_by=fixture_id_desc&has_played=1',
                'head_to_head_games': u'/v2/fixtures?team_ids=HAL,EDM&count=5&order_by=fixture_id_desc&has_played=1',
                'home_recent_games': u'/v2/fixtures?team_ids=HAL&count=5&order_by=fixture_id_desc&has_played=1'},
            'season_id': 99
        }]}
