from datetime import datetime

from fastapi import APIRouter, HTTPException

from errors import Missing
from models.pydantic.games import (
    GameDetailSchema,
    GameWithLeagueSchema
)
from services import games as service


router = APIRouter(prefix="/games", tags=["games"])


@router.get("/{game_id}")
async def get_game(game_id: int) -> GameDetailSchema:
    """Получить полную информацию о конкретном матче"""
    try:
        game = await service.get_game(game_id)
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return game


@router.get("/")
async def get_games_for_date(date: str) -> list[GameWithLeagueSchema]:
    """Получить список матчей за определенный день"""
    query_date = datetime.strptime(date, "%Y-%m-%d")
    games = await service.get_games_for_date(query_date)
    return games
