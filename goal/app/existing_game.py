import os
from .base import v2_route, app


@v2_route(app, '/v2/games')
def get_existing_games():
    games = [{'id': f.split('.db')[0]} for f in os.listdir('.') if f.endswith('.db')]
    return {
        'games': games
    }


@v2_route(app, '/v2/games', methods=['POST'])
def new_game():
    pass
