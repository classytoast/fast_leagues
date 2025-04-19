from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload

from database import async_session
from models.db.leagues import League, Season, Country
from models.pydantic.leagues import SeasonSchema, LeagueSchema


async def get_all_leagues() -> list[LeagueSchema]:
    async with async_session() as session:
        query = select(
            League.id,
            League.country,
            League.name,
            League.seasons
        ).options(
            selectinload(
                League.seasons.and_(
                    Season.id == select(
                        func.max(Season.id)
                    ).filter(
                        Season.league_id == League.id
                    ).scalar_subquery()
                )
            )
        ).options(
            joinedload(
                League.country
            )
        )
        result = await session.execute(query)
        leagues = result.all()
    return leagues


async def get_one_league(league_id: int) -> LeagueSchema | None:
    async with async_session() as session:
        query = select(
            League.id,
            League.country,
            League.name
        ).filter(
            League.id == league_id
        )
        league = await (session.execute(query)).scalars.one()
    return league


async def get_seasons(league_id: int) -> list[SeasonSchema]:
    return []


async def get_season(league_id: int, season_id: int) -> SeasonSchema | None:
    return []
