import requests
import functools
from goal.db import get_engine, Base, Country, Team, Competition
from sqlalchemy.orm import sessionmaker


def commit(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        retval = fn(self, *args, **kwargs)
        self.session.commit()
        return retval
    return wrapper


class BaseTestCase(object):
    SERVICE_LOCATION_PREFIX = 'http://localhost:5000'
    TEST_DATABASE_NAME = 'goal_integration_test.db'

    @commit
    def create_country(self, country_id, name):
        self.session.add(
            Country(country_id=country_id, name=name))

    @commit
    def create_team(self, **kwargs):
        self.session.add(Team(**kwargs))

    @commit
    def create_competition(self, **kwargs):
        self.session.add(Competition(**kwargs))

    def create_english_premier_league(self):
        self.create_competition(
            competition_id='EPL', country_id='ENG', name='Premier League',
            tier=1, promotion_to=None)

    def make_api_request(self, method, endpoint):
        fn = getattr(requests, method.lower())
        return fn('{}/{}'.format(self.SERVICE_LOCATION_PREFIX, endpoint))

    def setup(self):
        engine = get_engine(self.TEST_DATABASE_NAME)
        self.session = session = sessionmaker(bind=engine)()
        Base.session = session
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        self.create_country('ENG', 'England')
        self.create_country('ITA', 'Italy')
