import requests
from goal.db import get_engine, Base
from sqlalchemy.orm import sessionmaker
from fixture import FixtureMixin


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


class BaseTestCase(FixtureMixin):
    @classmethod
    def setup_class(cls):
        cls.engine = engine = get_engine(TEST_DATABASE_NAME)
        cls.session = session = sessionmaker(bind=engine)()
        Base.session = session

    def setup_method(self, method):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        self.create_country('CAN', 'Canada'),

    def make_api_request(cls, method, endpoint):
        fn = getattr(requests, method.lower())
        return fn('{}/{}'.format(SERVICE_LOCATION_PREFIX, endpoint))
