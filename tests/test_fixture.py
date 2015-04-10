from base import BaseTestCase


class TestFixture(BaseTestCase):
    @classmethod
    def assert_fixture(
            cls, fixture, home_team, away_team, home_score, away_score):
        assert fixture['home_team'] == home_team
        assert fixture['away_team'] == away_team
        assert fixture['home_score'] == home_score
        assert fixture['away_score'] == away_score

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
                'away_recent_games': '/v2/fixtures?team_ids=EDM&count=5&order_by=fixture_id_desc&has_played=1',
                'head_to_head_games': '/v2/fixtures?team_ids=HAL,EDM&count=5&order_by=fixture_id_desc&has_played=1',
                'home_recent_games': '/v2/fixtures?team_ids=HAL&count=5&order_by=fixture_id_desc&has_played=1'},
            'season_id': 99
        }]}

    def test_get_fixtures_played_fixtures(self, cd1_season1):
        fixtures = cd1_season1.fixtures
        fixtures[0].home_score, fixtures[0].away_score = 2, 0
        self.session.add(fixtures[0])
        self.session.commit()
        response = self.make_api_request(
            'GET', 'v2/fixtures?season_id=99&gameday=1')
        assert len(response.json()['fixtures']) == 1
        assert response.json() == {'fixtures': [{
            'away_score': 0,
            'away_team': 'EDM',
            'game_day': 1,
            'home_score': 2,
            'home_team': 'HAL',
            'id': 1,
            'links': {
                'away_recent_games': '/v2/fixtures?team_ids=EDM&count=5&order_by=fixture_id_desc&has_played=1',
                'head_to_head_games': '/v2/fixtures?team_ids=HAL,EDM&count=5&order_by=fixture_id_desc&has_played=1',
                'home_recent_games': '/v2/fixtures?team_ids=HAL&count=5&order_by=fixture_id_desc&has_played=1'},
            'season_id': 99
        }]}

    def test_get_fixtures_head_to_head(self, cd1_season1):
        fixtures = cd1_season1.fixtures
        for fixture in fixtures:
            if set([fixture.home_team_id, fixture.away_team_id]) == \
                    set(['HAL', 'EDM']):
                fixture.home_score, fixture.away_score = 2, 0
                self.session.add(fixture)
                self.session.commit()
        response = self.make_api_request(
            'GET',
            'v2/fixtures?team_ids=HAL,EDM&count=2&order_by=fixture_id_desc&has_played=1'
        )
        response = response.json()['fixtures']
        assert len(response) == 2
        self.assert_fixture(response[0], 'EDM', 'HAL', 2, 0)
        self.assert_fixture(response[1], 'HAL', 'EDM', 2, 0)

    def test_get_fixtures_recent_games(self, cd1_season1):
        fixtures = cd1_season1.fixtures
        for fixture in fixtures:
            if 'EDM' in (fixture.home_team_id, fixture.away_team_id):
                fixture.home_score, fixture.away_score = 2, 0
                self.session.add(fixture)
                self.session.commit()
        response = self.make_api_request(
            'GET',
            'v2/fixtures?team_ids=EDM&count=5&order_by=fixture_id_desc&has_played=1'
        )
        response = response.json()['fixtures']
        assert len(response) == 4
        self.assert_fixture(response[0], 'PEI', 'EDM', 2, 0)
        self.assert_fixture(response[1], 'EDM', 'HAL', 2, 0)
        self.assert_fixture(response[2], 'EDM', 'PEI', 2, 0)
        self.assert_fixture(response[3], 'HAL', 'EDM', 2, 0)
