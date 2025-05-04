from fastapi import APIRouter, HTTPException

from errors import Missing
from models.pydantic.persons import PlayerDetailsSchema, PersonDetailsSchema
from services import persons as service


router = APIRouter(prefix="", tags=["persons"])


@router.get("/players/{player_id}")
async def get_player(player_id: int) -> PlayerDetailsSchema:
    """Получить полную информацию о конкретном игроке"""
    try:
        player = await service.get_player(player_id)
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return player


@router.get("/managers/{manager_id}")
async def get_manager(manager_id: int) -> PersonDetailsSchema:
    """Получить полную информацию о конкретном тренере"""
    try:
        manager = await service.get_manager(manager_id)
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return manager
