from fastapi import APIRouter

from models.pydantic.leagues import LeagueSchema, SeasonSchema
from services import leagues as service

router = APIRouter(prefix="/leagues")


@router.get("/")
async def get_all_leagues() -> list[LeagueSchema]:
    leagues = await service.get_all_leagues()
    return leagues


@router.get("/{league_id}")
async def get_one_league(league_id: str) -> LeagueSchema | None:
    league = await service.get_one_league(int(league_id))
    return league


@router.get("/{league_id}/seasons")
async def get_seasons(league_id: str) -> list[SeasonSchema]:
    seasons = await service.get_seasons(int(league_id))
    return seasons


@router.get("/{league_id}/seasons/{season_id}")
async def get_season(league_id: str, season_id: str) -> SeasonSchema | None:
    season = await service.get_season(int(league_id), int(season_id))
    return season
