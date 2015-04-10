import functools
from goal.db import (
    get_engine, Base, Country, Team, Competition, Season, Fixture)
from sqlalchemy.orm import sessionmaker


TEST_DATABASE_NAME = 'goal_integration_test.db'


COMPETITIONS = [
    dict(competition_id="CD1", country_id="CAN",
         name="Canadian Division 1", tier=2,
         promotion_to="CPL", num_promoted=1),
    dict(competition_id="CPL", country_id="CAN",
         name="Canadian Premier League", tier=1,
         relegation_to="CD1", num_relegated=1),
]


SERVICE_LOCATION_PREFIX = 'http://localhost:5000'


def commit(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        retval = fn(self, *args, **kwargs)
        self.session.add(retval)
        self.session.commit()
        return retval
    return wrapper


class FixtureMixin(object):
    @classmethod
    @commit
    def create_country(cls, country_id, name):
        return Country(country_id=country_id, name=name)

    @classmethod
    @commit
    def create_team(cls, **kwargs):
        return Team(**kwargs)

    @classmethod
    @commit
    def create_competition(cls, **kwargs):
        return Competition(**kwargs)

    @classmethod
    @commit
    def create_season(cls, **kwargs):
        return Season(**kwargs)

    @classmethod
    @commit
    def create_fixture(cls, season_id, game_day, h, a):
        return Fixture(
            season_id=season_id,
            game_day=game_day,
            home_team_id=h, away_team_id=a)


class BaseTestCase(FixtureMixin):
    @classmethod
    def setup_class(cls):
        engine = get_engine(TEST_DATABASE_NAME)
        cls.session = session = sessionmaker(bind=engine)()
        Base.session = session
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        cls.create_country('CAN', 'Canada'),

        for competition in COMPETITIONS:
            cls.create_competition(**competition)
