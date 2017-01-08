import uuid
import flask
from goal.service import SERVICES
from .base import v2_route, app


def _get_table_by_season_id(season_id, game_day):
    table = SERVICES['season'].get_current_table(season_id, game_day)
    result = []
    for i, row in enumerate(table):
        team, stats = row
        table_row = {
            "id": uuid.uuid4().hex,
            "pos": i + 1,
            "team": team,
        }
        table_row.update(stats)
        result.append(table_row)
    return result


@v2_route(app, '/v2/tables')
def v2_table():
    assert 'season_id' in flask.request.args
    result = _get_table_by_season_id(flask.request.args['season_id'], None)
    return {
        'tables': result
    }
