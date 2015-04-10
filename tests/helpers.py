import requests
import functools
from goal.db import Country, Team, Competition, Season, Fixture
from nose.tools import eq_  # noqa


SERVICE_LOCATION_PREFIX = 'http://localhost:5000'


def commit(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        retval = fn(*args, **kwargs)
        session.commit()
        return retval
    return wrapper


@commit
def create_country(country_id, name):
    session.add(
        Country(country_id=country_id, name=name))


@commit
def create_team(**kwargs):
    session.add(Team(**kwargs))


@commit
def create_competition(**kwargs):
    session.add(Competition(**kwargs))


@commit
def create_season(**kwargs):
    season = Season(**kwargs)
    session.add(season)
    return season


@commit
def create_fixture(season_id, game_day, h, a):
    add(Fixture(
        season_id=season_id,
        game_day=game_day,
        home_team_id=h, away_team_id=a))
