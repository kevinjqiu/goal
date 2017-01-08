from .base import v2_route, app


@v2_route(app, '/v2/games')
def get_existing_games():
    return {
        'games': [
            {'id': 'abcdef'}  # TODO
        ]
    }


@v2_route(app, '/v2/games', methods=['POST'])
def new_game():
    pass
