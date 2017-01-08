from .base import v2_route, app
from goal.service import SERVICES


@v2_route(app, '/v2/teams/<string:id>')
def v2_get_team(id):
    return {
        "teams": [
            SERVICES['team'].get_by_id(id)
        ]
    }
