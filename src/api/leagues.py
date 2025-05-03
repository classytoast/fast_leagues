from fastapi import APIRouter, HTTPException

from errors import Missing
from models.pydantic.leagues import (
    LeagueWithCurrentSeasonSchema,
    LeagueCountrySchema,
    SeasonWithLeaderSchema,
    SeasonRelSchema
)
from services import leagues as service

router = APIRouter(prefix="/leagues", tags=["leagues and seasons"])


@router.get("/")
async def get_all_leagues() -> list[LeagueWithCurrentSeasonSchema]:
    """Получить список всех доступных лиг с информацией о текущем сезоне"""
    leagues = await service.get_all_leagues()
    return leagues


@router.get("/{league_id}")
async def get_one_league(league_id: int) -> LeagueCountrySchema:
    """Получить подробную информацию о конкретной лиге"""
    try:
        league = await service.get_one_league(league_id)
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return league


@router.get("/{league_id}/seasons")
async def get_seasons(league_id: int) -> list[SeasonWithLeaderSchema]:
    """Получить список сезонов для указанной лиги с информацией о лидерах в каждом сезоне"""
    try:
        seasons = await service.get_seasons(league_id)
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return seasons


@router.get("/{league_id}/seasons/{season_id}")
async def get_season(league_id: int, season_id: int) -> SeasonRelSchema:
    """Получить информацию о конкретном сезоне указанной лиги"""
    try:
        season = await service.get_season(league_id, season_id)
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return season
