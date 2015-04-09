from goal.db import get_engine, Base
from sqlalchemy.orm import sessionmaker
from lettuce import world
from helpers import create_country


TEST_DATABASE_NAME = 'goal_integration_test.db'


engine = get_engine(TEST_DATABASE_NAME)
world.session = session = sessionmaker(bind=engine)()
Base.session = session
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


world.countries = [
    create_country('ENG', 'England'),
    create_country('ITA', 'Italy'),
]
