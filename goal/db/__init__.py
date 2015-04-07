import yaml
import csv
import sqlalchemy
from .base import Base  # noqa
from .country import Country  # noqa
from .team import Team  # noqa
from .competition import Competition  # noqa
from .fixture import Fixture  # noqa
from .season import Season  # noqa


def get_engine(path_to_db):
    return sqlalchemy.create_engine('sqlite:///{}'.format(path_to_db))


def seed(session):
    seeds = [
        ('country', 'yaml'),
        ('competition', 'yaml'),
        ('team', 'csv'),
    ]
    for seed, ext in seeds:
        seed_file = 'seed/%s.%s' % (seed, ext)
        model_class = globals()[seed.capitalize()]

        load_fn = {
            "yaml": lambda f: yaml.load(f.read()),
            "csv": csv.DictReader,
        }[ext]

        with open(seed_file) as f:
            objects = load_fn(f)
            for obj in objects:
                try:
                    session.add(model_class(**obj))
                    session.commit()
                except sqlalchemy.exc.IntegrityError as e:
                    session.rollback()
                    print 'Cannot add {}: {}'.format(obj, str(e))


def bootstrap(session):
    engine = session.bind
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    seed(session)
