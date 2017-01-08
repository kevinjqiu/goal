from .base import v2_route, app
from goal.service import SERVICES


@v2_route(app, '/v2/fixtures/<int:fixture_id>/predict')
def v2_predict_score(fixture_id):
    home_score, away_score = SERVICES['fixture'].predict_score(fixture_id)
    return {
        'score': {
            'home': home_score,
            'away': away_score,
        }
    }
