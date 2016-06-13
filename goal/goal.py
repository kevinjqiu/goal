from argparse import ArgumentParser
from sqlalchemy.orm import sessionmaker
from .db import get_engine, bootstrap, Base
from .service import (
    SeasonService, CompetitionService, FixtureService, TeamService)
from .app import app
from .service import SERVICES


def start_season(year):
    competitions = SERVICES['competition'].get_all()
    for competition in competitions:
        SERVICES['season'].new_season(competition, year)


def main():
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    serve_parser = subparsers.add_parser('serve')
    serve_parser.add_argument('path_to_db')

    bootstrap_parser = subparsers.add_parser('bootstrap')
    bootstrap_parser.add_argument('path_to_db')

    console_parser = subparsers.add_parser('console')
    console_parser.add_argument('path_to_db')

    test_parser = subparsers.add_parser('test')
    test_parser.add_argument('path_to_db')

    args = parser.parse_args()

    engine = get_engine(args.path_to_db)
    session = sessionmaker(bind=engine)()
    Base.session = session

    SERVICES.update({
        'season': SeasonService(session),
        'competition': CompetitionService(session),
        'fixture': FixtureService(session),
        'team': TeamService(session),
    })

    if args.command == 'bootstrap':
        bootstrap(session)
        start_season(2016)
    elif args.command == 'serve':
        app.run(debug=True)
    elif args.command == 'console':
        import IPython
        from .db import *  # noqa
        IPython.embed()
    elif args.command == 'test':
        from .db import *  # noqa
        from sqlalchemy import and_
        from .predict import DixonRobinsonPredictor

        for game_day in xrange(30, 35):
            print
            print "Game Day %s" % game_day
            print "-------------------------"
            next_round = (
                Fixture.session.query(Fixture)
                .filter_by(season_id=6)
                .filter_by(game_day=game_day)
                .all()
            )

            query = (
                Fixture.session.query(Fixture)
                .filter_by(season_id=6)
                .filter(and_(
                    Fixture.home_score != None,  # noqa
                    Fixture.away_score != None
                ))
            )

            p = DixonRobinsonPredictor(query.all())

            for fixture in next_round:
                s1, s2 = p.predict_score(
                    fixture.home_team_id, fixture.away_team_id, 8)
                print "{} {}-{} {}".format(
                    fixture.home_team.name,
                    s1, s2,
                    fixture.away_team.name)
                SERVICES['fixture'].update_score(fixture.fixture_id, s1, s2)
