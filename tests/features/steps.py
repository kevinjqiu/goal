import json
from lettuce import step, world
from helpers import create_team, make_api_request, eq_


TEAMS = {
    'Man Utd': dict(team_id="MNU", name="Man Utd", country_id="ENG"),
    'Arsenal': dict(team_id="ARS", name="Arsenal", country_id="ENG"),
}


@step('I have a team "([^"]+)"')
def g0(step, team_name):
    create_team(**TEAMS[team_name])


@step('I call (GET|POST|PUT|DELETE) (.+)')
def w0(step, method, endpoint):
    response = make_api_request(method, endpoint)
    world.response = response


@step('I get an OK response')
def t0(step):
    assert world.response.status_code == 200


@step('The response matches (.+)')
def t1(step, response_body):
    eq_(world.response.json(),  json.loads(response_body))
