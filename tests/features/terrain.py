from goal.db import get_engine, Base
from sqlalchemy.orm import sessionmaker
from lettuce import world, before
from helpers import create_country, create_competition


TEST_DATABASE_NAME = 'goal_integration_test.db'


COMPETITIONS = [
    dict(competition_id="CD1", country_id="CAN",
         name="Canadian Division 1", tier=2,
         promotion_to="CPL", num_promoted=1),
    dict(competition_id="CPL", country_id="CAN",
         name="Canadian Premier League", tier=1,
         relegation_to="CD1", num_relegated=1),
]


@before.each_scenario
def setup(scenario):
    engine = get_engine(TEST_DATABASE_NAME)
    world.session = session = sessionmaker(bind=engine)()
    Base.session = session
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    create_country('CAN', 'Canada'),

    for competition in COMPETITIONS:
        create_competition(**competition)
