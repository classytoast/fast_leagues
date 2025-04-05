from models.pydantic.leagues import SeasonSchema, LeagueSchema
from repositories import leagues as data


async def get_all_leagues() -> list[LeagueSchema]:
    leagues = await data.get_all_leagues()
    return leagues


async def get_one_league(league_id: int) -> LeagueSchema | None:
    league = await data.get_one_league(league_id)
    return league


async def get_seasons(league_id: int) -> list[SeasonSchema]:
    seasons = await data.get_seasons(league_id)
    return seasons


async def get_season(league_id: int, season_id: int) -> SeasonSchema | None:
    season = await data.get_season(league_id, season_id)
    return season

