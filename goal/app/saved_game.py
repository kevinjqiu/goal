import os
from .base import v2_route, app


@v2_route(app, '/v2/games')
def get_saved_games():
    games = [{'id': f.split('.db')[0]} for f in os.listdir('.') if f.endswith('.db')]
    return {
        'games': games
    }


@v2_route(app, '/v2/games/<game_id>')
def get_saved_game(game_id):
    return {
        'gameId': game_id,
        'leagues': [
            {
                'countrId': 'ENG',
                'countryName': 'England',
                'leagueId': 'EPL',
                'leagueName': 'English Premier League',
            },
            {
                'countryId': 'ENG',
                'countryName': 'England',
                'leagueId': 'ECH',
                'leagueName': 'English Championship',
            },
            {
                'countryId': 'ENG',
                'countryName': 'England',
                'leagueId': 'EL1',
                'leagueName': 'English League One',
            },
            {
                'countryId': 'ENG',
                'countryName': 'England',
                'leagueId': 'EL2',
                'leagueName': 'English League Two',
            },
        ]
    }


@v2_route(app, '/v2/games', methods=['POST'])
def new_game():
    pass
