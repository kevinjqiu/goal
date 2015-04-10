import pytest
import functools
from goal.db import (
    Country, Team, Competition, Season, Fixture)


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

    @pytest.fixture
    def toronto(cls):
        return cls.create_team(team_id='TOR', name='Toronto FC',
                               country_id='CAN', current_competition_id='CPL')

    @pytest.fixture
    def montreal(cls):
        return cls.create_team(team_id='MON', name='Montreal Impact',
                               country_id='CAN', current_competition_id='CPL')

    @pytest.fixture
    def vancouver(cls):
        return cls.create_team(team_id='VAN', name='Vancouver',
                               country_id='CAN', current_competition_id='CPL')

    @pytest.fixture
    def ottawa(cls):
        return cls.create_team(team_id='OTT', name='Ottawa Fury',
                               country_id='CAN', current_competition_id='CPL')

    @pytest.fixture
    def halifax(cls):
        return cls.create_team(team_id='HAL', name='Halifax City',
                               country_id='CAN', current_competition_id='CD1')

    @pytest.fixture
    def edmonton(cls):
        return cls.create_team(team_id='EDM', name='Edmonton FC',
                               country_id='CAN', current_competition_id='CD1')

    @pytest.fixture
    def pei(cls):
        return cls.create_team(team_id='PEI', name='Prince Edward Islanders',
                               country_id='CAN', current_competition_id='CD1')

    @pytest.fixture
    def cpl(cls):
        cls.toronto, cls.montreal, cls.vancouver, cls.ottawa
        return cls.create_competition(
            competition_id='CPL', country_id='CAN',
            name='Canadian Premier League', tier=1, relegation_to='CD1',
            num_relegated=1)

    @pytest.fixture
    def cd1(cls):
        cls.halifax, cls.edmonton, cls.pei
        return cls.create_competition(
            competition_id='CD1', country_id='CAN',
            name='Canadian Division 1', tier=2,
            promotion_to='CPL', num_promoted=1)

    @pytest.fixture
    def cpl_season1(cls):
        CPL_SEASON1_ID = 66
        cls.cpl
        season = cls.create_season(**dict(
            season_id=CPL_SEASON1_ID,
            competition_id='CPL',
            start_year=2015, end_year=2015))
        teams = ['TOR', 'MTL', 'VAN', 'OTT']
        cls.create_fixture(CPL_SEASON1_ID, 1, teams[0], teams[3])
        cls.create_fixture(CPL_SEASON1_ID, 1, teams[1], teams[2])

        cls.create_fixture(CPL_SEASON1_ID, 2, teams[0], teams[2])
        cls.create_fixture(CPL_SEASON1_ID, 2, teams[1], teams[3])

        cls.create_fixture(CPL_SEASON1_ID, 3, teams[0], teams[1])
        cls.create_fixture(CPL_SEASON1_ID, 3, teams[2], teams[3])

        cls.create_fixture(CPL_SEASON1_ID, 4, teams[3], teams[0])
        cls.create_fixture(CPL_SEASON1_ID, 4, teams[2], teams[1])

        cls.create_fixture(CPL_SEASON1_ID, 5, teams[2], teams[0])
        cls.create_fixture(CPL_SEASON1_ID, 5, teams[3], teams[1])

        cls.create_fixture(CPL_SEASON1_ID, 6, teams[1], teams[0])
        cls.create_fixture(CPL_SEASON1_ID, 6, teams[3], teams[2])
        return season

    @pytest.fixture
    def cd1_season1(cls):
        CD1_SEASON1_ID = 99
        cls.cd1
        season = cls.create_season(**dict(
            season_id=CD1_SEASON1_ID,
            competition_id='CD1',
            start_year=2015, end_year=2015))

        teams = ['HAL', 'EDM', 'PEI']
        cls.create_fixture(CD1_SEASON1_ID, 1, teams[0], teams[1])
        cls.create_fixture(CD1_SEASON1_ID, 2, teams[0], teams[2])
        cls.create_fixture(CD1_SEASON1_ID, 3, teams[1], teams[2])
        cls.create_fixture(CD1_SEASON1_ID, 4, teams[1], teams[0])
        cls.create_fixture(CD1_SEASON1_ID, 5, teams[2], teams[0])
        cls.create_fixture(CD1_SEASON1_ID, 6, teams[2], teams[1])

        return season
