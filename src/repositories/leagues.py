from sqlalchemy import select, text

from database import async_session
from models.db.leagues import League
from models.pydantic.leagues import SeasonSchema, LeagueSchema, CountrySchema


async def get_all_leagues() -> list[LeagueSchema]:
    async with async_session() as session:
        query = text("""
            WITH last_seasons AS (
                SELECT 
                    MAX(id) AS id,
                    league_id,
                    name
                FROM
                    seasons
                GROUP BY
                    league_id
            )
            SELECT
                l.id,
                l.name,
                c.id,
                c.name,
                s.id,
                s.name
            FROM
                leagues AS l
            INNER JOIN last_seasons AS s
                ON s.league_id = l.id 
            INNER JOIN countries AS c
                ON c.id = l.country_id
        """)
        result = await session.execute(query)
        leagues = result.all()

    pydantic_leagues = map_to_league_schemas(leagues)
    return pydantic_leagues


def map_to_league_schemas(rows: list[tuple]) -> list[LeagueSchema]:
    leagues = []
    for row in rows:
        league_id, league_name, country_id, country_name, season_id, season_name = row

        leagues.append(LeagueSchema(
            id=league_id,
            name=league_name,
            country=CountrySchema(id=country_id, name=country_name),
            current_season=SeasonSchema(id=season_id, name=season_name, leader_id=0, leader_name="mock_team")
        ))

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
