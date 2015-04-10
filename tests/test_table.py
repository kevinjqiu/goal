from base import BaseTestCase


def set_score(fixture, home_score, away_score):
    fixture.home_score, fixture.away_score = home_score, away_score


class TestTableGet(BaseTestCase):
    def test_get_table_empty(self, cd1_season1):
        response = self.make_api_request('GET', 'v2/tables?season_id=99').json()
        assert len(response['tables']) == 3
        for pos in response['tables']:
            for pre in ('', 'h_', 'a_'):
                for field in ('win', 'draw', 'loss', 'gf', 'ga', 'gd'):
                    assert pos[pre + field] == 0

    def test_get_table_complete(self, cd1_season1):
        fixtures = cd1_season1.fixtures
        set_score(fixtures[0], 2, 0)
        set_score(fixtures[1], 3, 0)
        set_score(fixtures[2], 2, 2)
        set_score(fixtures[3], 2, 1)
        set_score(fixtures[4], 2, 2)
        set_score(fixtures[5], 4, 1)
        self.session.add(cd1_season1)
        self.session.commit()
        response = self.make_api_request('get', 'v2/tables?season_id=99')
        tables = response.json()['tables']
        assert tables[0]['team'] == 'HAL'
        assert tables[0]['h_win'] == 2
        assert tables[0]['a_draw'] == 1
        assert tables[0]['a_loss'] == 1
        assert tables[0]['gf'] == 8
        assert tables[0]['ga'] == 4

        assert tables[1]['team'] == 'PEI'
        assert tables[1]['h_win'] == 1
        assert tables[1]['h_draw'] == 1
        assert tables[1]['a_draw'] == 1
        assert tables[1]['a_loss'] == 1
        assert tables[1]['gf'] == 8
        assert tables[1]['ga'] == 8

        assert tables[2]['team'] == 'EDM'
        assert tables[2]['h_win'] == 1
        assert tables[2]['h_draw'] == 1
        assert tables[2]['a_loss'] == 2
        assert tables[2]['gf'] == 5
        assert tables[2]['ga'] == 9
