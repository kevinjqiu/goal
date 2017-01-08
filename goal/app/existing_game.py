from .base import v2_route, app


@v2_route(app, '/v2/existingGames')
def existing_games():
    return {
        'savedGames': [
            {'id': 'abcdef'}  # TODO
        ]
    }
