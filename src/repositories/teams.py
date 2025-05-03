from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload, joinedload

from database import async_session
from errors import Missing
from models.db.teams import Team
from models.pydantic.teams import TeamRelSchema


async def get_all_teams() -> list[TeamRelSchema]:
    async with async_session() as session:
        query = select(
            Team
        ).options(
            joinedload(Team.country)
        ).options(
            selectinload(Team.seasons)
        )
        result = await session.execute(query)
        result = result.scalars().all()

    return [TeamRelSchema.model_validate(row, from_attributes=True) for row in result]


async def get_one_team(team_id: int) -> TeamRelSchema:
    async with async_session() as session:
        query = select(
            Team
        ).options(
            joinedload(Team.country)
        ).options(
            selectinload(Team.seasons)
        ).filter(
            Team.id == team_id
        )
        result = await session.execute(query)
        try:
            result = result.scalars().one()
        except NoResultFound:
            raise Missing(f"команда с id - {team_id} не найдена")

    return TeamRelSchema.model_validate(result, from_attributes=True)
