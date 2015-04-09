import json
from lettuce import step, world
from helpers import (
    create_team, create_competition, create_fixture,
    create_season,
    make_api_request, eq_)


TEAMS = {
    'Toronto': dict(
        team_id="TOR", name="Toronto FC", country_id="CAN",
        current_competition_id='CPL'),
    'Montreal': dict(
        team_id="MTL", name="Montreal Impact", country_id="CAN",
        current_competition_id='CPL'),
    'Vancouver': dict(
        team_id="VAN", name="Vancouver Whitecaps", country_id="CAN",
        current_competition_id='CPL'),
    'Ottawa': dict(
        team_id="OTT", name="Ottawa Fury", country_id="CAN",
        current_competition_id='CD1'),
    'Edmonton': dict(
        team_id="EDM", name="FC Edmonton", country_id="CAN",
        current_competition_id='CD1'),
    'Halifax': dict(
        team_id="HAL", name="Halifax City", country_id="CAN",
        current_competition_id='CD1'),
}


@step('I have a team "([^"]+)"$')
def g0(step, team_name):
    create_team(**TEAMS[team_name])


@step('I call (GET|POST|PUT|DELETE) (.+)')
def w0(step, method, endpoint):
    response = make_api_request(method, endpoint)
    world.response = response


def start_season(competition_id, season_id):
    if competition_id == 'CPL':
        props = dict(
            competition_id='CPL', start_year=2015, end_year=2015)
        if season_id is not None:
            props['season_id'] = season_id
        season = create_season(**props)
        season_id = season.season_id
        teams = ('TOR', 'MTL', 'VAN')
        create_fixture(season_id, 1, teams[0], teams[1])
        create_fixture(season_id, 2, teams[0], teams[2])
        create_fixture(season_id, 3, teams[1], teams[2])
        create_fixture(season_id, 4, teams[1], teams[0])
        create_fixture(season_id, 5, teams[2], teams[0])
        create_fixture(season_id, 6, teams[2], teams[1])

@step('I start a new ([^\s]+) season with id: (\d+)')
def w1(step, competition_id, season_id):
    start_season(competition_id, season_id)

@step('I start a new ([^\s]+) season')
def w2(step, competition_id):
    start_season(competition_id, None)


@step('I get a response: (\d+)')
def t0(step, response_code):
    eq_(world.response.status_code, int(response_code))


@step('The response matches (.+)')
def t1(step, response_body):
    eq_(world.response.json(),  json.loads(response_body))


@step('I get (\d+) (\w+)')
def t2(step, num_entities, entity_name):
    eq_(len(world.response.json()[entity_name]), int(num_entities))
