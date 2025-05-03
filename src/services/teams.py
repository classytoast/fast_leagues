from models.pydantic.teams import TeamRelSchema
from repositories import teams as data


async def get_all_teams() -> list[TeamRelSchema]:
    teams = await data.get_all_teams()
    return teams


async def get_one_team(team_id: int) -> TeamRelSchema:
    team = await data.get_one_team(team_id)
    return team

