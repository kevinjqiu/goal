import json
from lettuce import step, world
from helpers import create_team, create_competition, make_api_request, eq_


TEAMS = {
    'Man Utd': dict(team_id="MNU", name="Man Utd", country_id="ENG"),
    'Arsenal': dict(team_id="ARS", name="Arsenal", country_id="ENG"),
}


COMPETITIONS = {
    'EPL': dict(competition_id="EPL", country_id="ENG",
                name="Premier League", tier=1),
}


@step('I have a team "([^"]+)"$')
def g0(step, team_name):
    create_team(**TEAMS[team_name])


@step('I have a team "([^"]+)" in (.+)$')
def g1(step, team_name, competition_id):
    create_competition(**COMPETITIONS[competition_id])
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
