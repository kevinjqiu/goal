import uuid
import flask
import functools
from .service import SERVICES
from flask.ext.cors import cross_origin


DEFAULT_START_YEAR = 2015


class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__json__'):
            return o.__json__()
        return super(MyJSONEncoder, self).default(o)


app = flask.Flask(__name__)
app.json_encoder = MyJSONEncoder


def json_response(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        return flask.jsonify(result)
    return wrapper


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


@app.route('/current_seasons')
@cross_origin()
@json_response
def get_current_seasons():
    start_year = flask.request.args.get('start_year', 2015)
    return {
        'current_seasons': SERVICES['season'].get_current_seasons(start_year)
    }


def v2_route(app, route, *args, **kwargs):
    def decorator(fn):
        return app.route(route, *args, **kwargs)(
            cross_origin()(json_response(fn)))

    return decorator


@v2_route(app, '/v2/tables')
def v2_table():
    assert 'season_id' in flask.request.args
    result = _get_table_by_season_id(flask.request.args['season_id'], None)
    return {
        'tables': result
    }


@v2_route(app, '/v2/teams/<string:id>')
def v2_get_team(id):
    return {
        "teams": [
            SERVICES['team'].get_by_id(id)
        ]
    }


@v2_route(app, '/v2/fixtures/<int:fixture_id>/predict')
def v2_predict_score(fixture_id):
    home_score, away_score = SERVICES['fixture'].predict_score(fixture_id)
    return {
        'score': {
            'home': home_score,
            'away': away_score,
        }
    }


@v2_route(app, '/v2/seasons/<int:season_id>')
def v2_get_season(season_id):
    season = SERVICES['season'].get_by_season_id(season_id)
    return {
        'seasons': [season],
    }


@v2_route(app, '/v2/seasons', methods=['POST'])
def v2_create_season():
    country_id = flask.request.json['country_id']
    competition = SERVICES['competition'].get_top_tier_in_country(country_id)
    seasons = SERVICES['season'].get_by_competition_id(
        competition.competition_id)
    if len(seasons) > 0:
        season = seasons[-1]
        SERVICES['season'].end_season(season)
    else:
        SERVICES['season'].new_season(competition, DEFAULT_START_YEAR)
    return {}


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
