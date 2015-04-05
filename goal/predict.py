import math
from collections import defaultdict
from random import random
from bisect import bisect


def poisson(mean, k):
    return math.exp(-mean) * (mean ** k) / math.factorial(k)


def poisson_histogram(mean, until):
    return [(x, round(poisson(mean, x), 2)) for x in xrange(until + 1)]


def weighted_choice(choices):
    """choices in the form of: [(choice1, percent1), ..., (choiceN, percentN)]
    """
    values, weights = zip(*choices)
    total = 0
    cumul_weights = []
    for w in weights:
        total += w
        cumul_weights.append(total)

    x = random() * total
    i = bisect(cumul_weights, x)
    return values[i]


class Stats(object):
    def __init__(self):
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        self.attack_strength = None
        self.defence_weakness = None

    def __repr__(self):
        return "p: {}, gf: {}, ga: {}, as: {}, dw: {}".format(
            self.points, self.goals_for, self.goals_against,
            self.attack_strength, self.defence_weakness,
        )


class SimplePredictor(object):
    def __init__(self, past_fixtures):
        self.past_fixtures = past_fixtures
        self.team_stats = self.get_team_stats_from_existing_fixtures(
            self.past_fixtures)

    def get_team_stats_from_existing_fixtures(self, fixtures):
        def agg(aggregate, fixture):
            home_stats = aggregate[fixture.home_team_id]
            away_stats = aggregate[fixture.away_team_id]

            if fixture.home_score > fixture.away_score:
                home_stats.points += 3
            elif fixture.home_score < fixture.away_score:
                away_stats.points += 3
            else:
                home_stats.points += 1
                away_stats.points += 1
            home_stats.goals_for += fixture.home_score
            away_stats.goals_for += fixture.away_score
            home_stats.goals_against += fixture.away_score
            away_stats.goals_against += fixture.home_score

            return aggregate

        result = reduce(agg, fixtures, defaultdict(Stats))

        average_team_goals = 1.0 * sum([
            stats.goals_for for stats in result.values()]) / len(result)

        average_team_concedes = 1.0 * sum([
            stats.goals_against for stats in result.values()]) / len(result)

        for team, stats in result.iteritems():
            stats.attack_strength = 1.0 * stats.goals_for / average_team_goals
            stats.defence_weakness = (
                1.0 * stats.goals_against / average_team_concedes)

        return result

    def predict_score(self, team1, team2):
        average_home_goals = 1.0 * sum([
            fixture.home_score for fixture in self.past_fixtures
        ]) / len(self.past_fixtures)
        average_away_goals = 1.0 * sum([
            fixture.away_score for fixture in self.past_fixtures
        ]) / len(self.past_fixtures)

        team_stats = self.team_stats

        expected_goal_1 = (
            average_home_goals * team_stats[team1].attack_strength
            * average_home_goals * team_stats[team2].defence_weakness
        )
        expected_goal_2 = (
            average_away_goals * team_stats[team2].attack_strength
            * average_away_goals * team_stats[team1].defence_weakness
        )
        goals_probability_distribution_1 = poisson_histogram(
            expected_goal_1, 6)
        goals_probability_distribution_2 = poisson_histogram(
            expected_goal_2, 6)

        return (
            weighted_choice(goals_probability_distribution_1),
            weighted_choice(goals_probability_distribution_2),
        )
