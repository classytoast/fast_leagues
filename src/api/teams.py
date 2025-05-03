from fastapi import APIRouter, HTTPException

from errors import Missing
from models.pydantic.teams import TeamRelSchema
from services import teams as service


router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/")
async def get_all_teams() -> list[TeamRelSchema]:
    teams = await service.get_all_teams()
    return teams


@router.get("/{team_id}")
async def get_one_team(team_id: int) -> TeamRelSchema:
    try:
        team = await service.get_one_team(team_id)
    except Missing as m:
        raise HTTPException(status_code=404, detail=m.msg)
    return team
