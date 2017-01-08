import flask
from .base import app, cross_origin, json_response, v2_route
from goal.service import SERVICES


@app.route('/current_seasons')
@cross_origin()
@json_response
def get_current_seasons():
    start_year = flask.request.args.get('start_year', 2015)
    return {
        'current_seasons': SERVICES['season'].get_current_seasons(start_year)
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
    competitions = SERVICES['competition'].get_by_country_id(country_id)
    competition = competitions[0]
    seasons = SERVICES['season'].get_by_competition_id(
        competition.competition_id)
    if len(seasons) > 0:
        season = seasons[-1]
        SERVICES['season'].end_season(season)
    else:
        for competition in competitions:
            SERVICES['season'].new_season(competition, DEFAULT_START_YEAR)
    return {}
