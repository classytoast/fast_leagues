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
    leagues = await service.get_all_leagues()
    return leagues


@router.get("/{league_id}")
async def get_one_league(league_id: str) -> LeagueCountrySchema:
    try:
        league = await service.get_one_league(int(league_id))
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return league


@router.get("/{league_id}/seasons")
async def get_seasons(league_id: str) -> list[SeasonWithLeaderSchema]:
    try:
        seasons = await service.get_seasons(int(league_id))
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return seasons


@router.get("/{league_id}/seasons/{season_id}")
async def get_season(league_id: str, season_id: str) -> SeasonRelSchema:
    try:
        season = await service.get_season(int(league_id), int(season_id))
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return season
