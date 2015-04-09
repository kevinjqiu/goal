import json
from lettuce import step, world
from helpers import create_team, create_competition, make_api_request, eq_


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


@step('I have a team "([^"]+)" in (.+)$')
def g1(step, team_name, competition_id):
    props = TEAMS[team_name]
    props['current_competition_id'] = competition_id
    create_team(**props)


@step('I call (GET|POST|PUT|DELETE) (.+)')
def w0(step, method, endpoint):
    response = make_api_request(method, endpoint)
    world.response = response


@step('I get a response: (\d+)')
def t0(step, response_code):
    eq_(world.response.status_code, int(response_code))


@step('The response matches (.+)')
def t1(step, response_body):
    eq_(world.response.json(),  json.loads(response_body))
