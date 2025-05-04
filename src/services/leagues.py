from models.pydantic.leagues import (
    LeagueWithCurrentSeasonSchema,
    LeagueCountrySchema,
    SeasonWithLeaderSchema,
    SeasonRelSchema,
    SeasonWithPlayersSchema
)
from repositories import leagues as data


async def get_all_leagues() -> list[LeagueWithCurrentSeasonSchema]:
    """Получает список всех доступных лиг с информацией о текущем сезоне"""
    leagues = await data.get_all_leagues()
    return leagues


async def get_one_league(league_id: int) -> LeagueCountrySchema:
    """Получает подробную информацию о конкретной лиге"""
    league = await data.get_one_league(league_id)
    return league


async def get_seasons(league_id: int) -> list[SeasonWithLeaderSchema]:
    """Получает список всех сезонов указанной лиги с информацией о лидерах в каждом сезоне"""
    seasons = await data.get_seasons(league_id)
    return seasons


async def get_season(league_id: int, season_id: int) -> SeasonRelSchema:
    """Получает детальную информацию о конкретном сезоне лиги"""
    season = await data.get_season(league_id, season_id)
    return season


async def get_players_in_season(league_id: int, season_id: int) -> SeasonWithPlayersSchema:
    """Получает информацию об игроках в конкретном сезоне лиги"""
    season = await data.get_players_in_season(league_id, season_id)
    return season

