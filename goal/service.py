import random
import functools
from sqlalchemy import and_, or_
from .db import Competition, Season, Fixture, Country, Team
from collections import defaultdict
from .predict import SimplePredictor


SERVICES = {}


def json(fn):
    if hasattr(fn, '__json__'):
        return fn.__json__()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        if isinstance(result, (list, tuple)):
            return [
                obj.__json__() for obj in result]
        else:
            return result.__json__()
    return wrapper


def _shift(array):
    return array[1:] + [array[0]]


class Service(object):
    def __init__(self, session):
        self.session = session


class SeasonService(Service):
    def get_num_of_gamedays(self, season_id):
        return Season.get_num_of_gamedays(season_id)

    def get_current_seasons(self, start_year):
        # TODO: Use start_year
        retval = []
        for country in self.session.query(Country).all():
            cc = {
                'country': json(country),
                'seasons': []
            }
            for competition in country.competitions:
                if len(competition.seasons) > 0:
                    season = competition.seasons[-1]
                    competition = season.competition
                    season = json(season)
                    season['competition'] = json(competition)
                    season['next_game_day'] = Season.get_next_game_day(season['id'])
                    cc['seasons'].append(season)
            retval.append(cc)
        return retval

    def get_by_competition_id(self, competition_id):
        return (
            self.session.query(Season)
            .filter_by(competition_id=competition_id)
            .order_by(Season.start_year.desc())
            .all()
        )

    def get_by_season_id(self, season_id):
        return Season.get_by_id(season_id)

    def get_fixtures(
            self, season_id, game_day, team_ids,
            order_by, count, has_played=None):
        query = self.session.query(Fixture)
        if season_id is not None:
            query = query.filter_by(season_id=season_id)
        if game_day is not None:
            query = query.filter_by(game_day=game_day)
        if team_ids is not None:
            team_ids = team_ids.split(',')
            conj = or_ if len(team_ids) == 1 else and_
            query = query.filter(conj(
                Fixture.home_team_id.in_(team_ids),
                Fixture.away_team_id.in_(team_ids)))
        if has_played is not None:
            if bool(has_played):
                query = query.filter(and_(
                    Fixture.home_score != None,
                    Fixture.away_score != None))
            else:
                query = query.filter(and_(
                    Fixture.home_score == None,
                    Fixture.away_score == None))
        if order_by is not None:
            segments = order_by.split('_')
            direction = segments[-1]
            field_name = '_'.join(segments[:-1])
            sort_fn = getattr(getattr(Fixture, field_name), direction)
            query = query.order_by(sort_fn())
        if count is not None:
            query = query.limit(count)
        return query.all()

    def get_current_table(self, season_id, game_day=None):
        season = Season.get_by_id(season_id)
        query = (
            self.session.query(Fixture)
            .filter(Fixture.season_id == season_id)
            .filter(Fixture.home_score != None)  # noqa
            .filter(Fixture.away_score != None)
        )
        if game_day is not None:
            query = query.filter(Fixture.game_day <= game_day)

        table_rows = defaultdict(lambda: defaultdict(int))

        fixtures = query.all()
        teams = season.competition.current_teams

        for team in teams:
            table_rows[team.team_id]['team_name'] = team.name
            for home_or_away in ('h_', 'a_'):
                for field in ('win', 'draw', 'loss', 'gf', 'ga', 'gd'):
                    table_rows[team.team_id][home_or_away + field] = 0

        for fixture in fixtures:
            home_team_id, away_team_id = \
                fixture.home_team_id, fixture.away_team_id

            table_rows[home_team_id]['team_name'] = fixture.home_team.name
            table_rows[home_team_id]['h_gf'] += fixture.home_score
            table_rows[home_team_id]['h_ga'] += fixture.away_score

            table_rows[away_team_id]['team_name'] = fixture.away_team.name
            table_rows[away_team_id]['a_gf'] += fixture.away_score
            table_rows[away_team_id]['a_ga'] += fixture.home_score

            if fixture.home_score > fixture.away_score:
                table_rows[home_team_id]['h_win'] += 1
                table_rows[away_team_id]['a_loss'] += 1
            elif fixture.home_score < fixture.away_score:
                table_rows[home_team_id]['h_loss'] += 1
                table_rows[away_team_id]['a_win'] += 1
            else:
                table_rows[home_team_id]['h_draw'] += 1
                table_rows[away_team_id]['a_draw'] += 1

        for team_stat in table_rows.values():
            team_stat['pld'] = sum([
                team_stat['h_win'], team_stat['h_draw'], team_stat['h_loss'],
                team_stat['a_win'], team_stat['a_draw'], team_stat['a_loss'],
            ])
            team_stat['pts'] = (
                3 * (team_stat['h_win'] + team_stat['a_win']) +
                1 * (team_stat['h_draw'] + team_stat['a_draw'])
            )
            team_stat['win'] = team_stat['h_win'] + team_stat['a_win']
            team_stat['draw'] = team_stat['h_draw'] + team_stat['a_draw']
            team_stat['loss'] = team_stat['h_loss'] + team_stat['a_loss']
            team_stat['gf'] = team_stat['h_gf'] + team_stat['a_gf']
            team_stat['ga'] = team_stat['h_ga'] + team_stat['a_ga']
            team_stat['gd'] = team_stat['gf'] - team_stat['ga']

        def cmp_fn(row1, row2):
            _, t1 = row1
            _, t2 = row2
            if t1['pts'] > t2['pts']:
                return -1
            if t1['pts'] < t2['pts']:
                return 1
            if t1['gd'] > t2['gd']:
                return -1
            if t1['gd'] < t2['gd']:
                return 1
            if t1['gf'] > t2['gf']:
                return -1
            if t1['gf'] < t2['gf']:
                return 1
            return 0

        return sorted(table_rows.items(), cmp_fn)

    def end_season(self, season):
        assert season.__json__()['next_game_day'] is None, \
            "Season is not yet finished"
        competition = season.competition
        lower_tier_competition = season.competition.lower_tier_competition
        lower_tier_season = None
        if lower_tier_competition is not None:
            try:
                lower_tier_season = lower_tier_competition.seasons[-1]
            except IndexError:
                pass

        # send the bottom n teams to the lower tier
        table = self.get_current_table(season.season_id)
        if lower_tier_season and competition.num_relegated:
            bottom_positions = table[-competition.num_relegated:]
            for team_id, _ in bottom_positions:
                team = Team.get_by_id(team_id)
                team.current_competition = lower_tier_competition
                self.session.add(team)
        # take the top n teams from the lower tier
        if lower_tier_season and lower_tier_competition.num_promoted:
            lower_tier_table = self.get_current_table(
                lower_tier_season.season_id)
            top_positions = \
                lower_tier_table[:lower_tier_competition.num_promoted]
            for team_id, _ in top_positions:
                team = Team.get_by_id(team_id)
                team.current_competition = competition
                self.session.add(team)
        self.session.commit()
        self.new_season(competition, season.end_year)
        if lower_tier_competition is not None and lower_tier_season is not None:
            self.new_season(lower_tier_competition, lower_tier_season.end_year)

    def new_season(self, competition, start_year):
        end_year = start_year + 1

        season = Season(
            start_year=start_year,
            end_year=end_year,
        )
        season.competition = competition
        teams = competition.current_teams
        fixtures = self.schedule_fixtures(teams)
        season.fixtures = fixtures
        self.session.add(season)
        self.session.commit()
        return season

    def schedule_fixtures(self, teams):
        teams = list(teams)
        num_teams = len(teams)
        num_rounds = num_teams - 1

        if num_teams % 2 == 1:
            teams.append('GHOST')
        random.shuffle(teams)

        fixtures = []
        for r in xrange(num_rounds):
            for i in xrange(num_teams / 2):
                home, away = teams[i], teams[-(i+1)]
                if home == 'GHOST' or away == 'GHOST':
                    continue

                if r % 2 == 0:
                    home, away = away, home

                fixture = Fixture(
                    game_day=r+1,
                    home_team=home,
                    away_team=away,
                )
                fixtures.append(fixture)

            first, rest = teams[0], teams[1:]
            teams = [first] + _shift(rest)

        # generate the mirror fixtures
        for fixture in list(fixtures):
            fixtures.append(Fixture(
                game_day=fixture.game_day+num_teams-1,
                home_team=fixture.away_team,
                away_team=fixture.home_team
            ))

        return fixtures


class CompetitionService(Service):
    def get_all(self):
        return self.session.query(Competition).all()

    def get_by_id(self, competition_id):
        return Competition.get_by_id(competition_id)

    def get_by_country_id(self, country_id):
        return Competition.get_by_country_id(country_id)


class FixtureService(Service):
    def update_score(self, fixture_id, home_score, away_score):
        fixture = self.session.query(Fixture).filter_by(
            fixture_id=fixture_id).one()
        fixture.home_score = home_score
        fixture.away_score = away_score
        self.session.add(fixture)
        self.session.commit()

    def predict_score(self, fixture_id):
        fixture = Fixture.get_by_id(fixture_id)
        if fixture.game_day == 1:
            return 0, 0

        past_fixtures = Fixture.get_past_fixtures(
            fixture.season_id, fixture.game_day)

        predictor = SimplePredictor(past_fixtures)
        return predictor.predict_score(
            fixture.home_team_id, fixture.away_team_id)


class TeamService(Service):
    def get_by_id(self, id):
        return Team.get_by_id(id)
