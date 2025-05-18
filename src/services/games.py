from datetime import datetime

from repositories import games as data
from models.pydantic.games import (
    GameDetailSchema,
    GameWithLeagueSchema
)


async def get_game(game_id: int) -> GameDetailSchema:
    """Получает полную информацию о конкретном матче по его ID"""
    game = await data.get_game(game_id)
    return game


async def get_games_for_date(date: datetime) -> list[GameWithLeagueSchema]:
    """Получает список матчей за определенный день"""
    games = await data.get_games_for_date(date)
    return games
