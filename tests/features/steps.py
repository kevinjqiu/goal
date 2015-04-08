from lettuce import step, world


@step('Given I have a team "([^"]+)" in "([^"]+)"')
def s(step, team_name, country):
    world.team = create_team(
        team_id=team_name,
        name=team_name,
        country_id=country)
