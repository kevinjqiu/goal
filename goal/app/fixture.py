import flask
from goal.service import SERVICES
from .base import v2_route, app


@v2_route(app, '/v2/fixtures')
def v2_get_fixtures():
    season_id = flask.request.args.get('season_id', None)
    gameday = flask.request.args.get('gameday', None)
    team_ids = flask.request.args.get('team_ids', None)
    count = flask.request.args.get('count', None)
    order_by = flask.request.args.get('order_by', None)
    has_played = flask.request.args.get('has_played', None)

    fixtures = [
        item.__json__() for item in
        SERVICES['season'].get_fixtures(
            season_id, gameday, team_ids, order_by, count, has_played)
    ]

    for fixture in fixtures:
        recent_games_url = (
            '/v2/fixtures?team_ids={}'
            '&count=5'
            '&order_by=fixture_id_desc'
            '&has_played=1')
        home_recent_games_url = recent_games_url.format(fixture['home_team'])
        away_recent_games_url = recent_games_url.format(fixture['away_team'])
        head_to_head_url = (
            '/v2/fixtures?team_ids={},{}'
            '&count=5'
            '&order_by=fixture_id_desc'
            '&has_played=1'
            .format(fixture['home_team'], fixture['away_team'])
        )

        fixture['links'] = {
            'home_recent_games': home_recent_games_url,
            'away_recent_games': away_recent_games_url,
            'head_to_head_games': head_to_head_url,
        }

    return {
        'fixtures': fixtures
    }


@v2_route(app, '/v2/fixtures/<int:fixture_id>', methods=['PUT'])
def v2_update_fixture_score(fixture_id):
    req_obj = flask.request.json['fixture']
    home_score, away_score = req_obj['home_score'], req_obj['away_score']
    SERVICES['fixture'].update_score(fixture_id, home_score, away_score)
    return {}
