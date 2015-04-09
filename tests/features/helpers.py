import requests
import functools
from lettuce import world
from goal.db import Country, Team, Competition, Season, Fixture
from nose.tools import eq_  # noqa


SERVICE_LOCATION_PREFIX = 'http://localhost:5000'


def commit(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        retval = fn(*args, **kwargs)
        world.session.commit()
        return retval
    return wrapper


@commit
def create_country(country_id, name):
    world.session.add(
        Country(country_id=country_id, name=name))


@commit
def create_team(**kwargs):
    world.session.add(Team(**kwargs))


@commit
def create_competition(**kwargs):
    world.session.add(Competition(**kwargs))


@commit
def create_season(**kwargs):
    season = Season(**kwargs)
    world.session.add(season)
    return season


@commit
def create_fixture(season_id, game_day, h, a):
    world.session.add(Fixture(
        season_id=season_id,
        game_day=game_day,
        home_team_id=h, away_team_id=a))


def make_api_request(method, endpoint):
    fn = getattr(requests, method.lower())
    return fn('{}/{}'.format(SERVICE_LOCATION_PREFIX, endpoint))
