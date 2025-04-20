from sqlalchemy import select, text, and_
from sqlalchemy.exc import NoResultFound

from database import async_session
from errors import Missing
from models.db.leagues import League, Country, Season
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
        result = result.all()

    return to_many_leagues_schemas(result)


def to_many_leagues_schemas(rows: list[tuple]) -> list[LeagueSchema]:
    result = []
    for row in rows:
        league_id, league_name, country_id, country_name, season_id, season_name = row

        result.append(LeagueSchema(
            id=league_id,
            name=league_name,
            country=CountrySchema(id=country_id, name=country_name),
            current_season=SeasonSchema(id=season_id, name=season_name, leader_id=0, leader_name="mock_team")
        ))

    return result


async def get_one_league(league_id: int) -> LeagueSchema:
    async with async_session() as session:
        query = select(
            League.id,
            League.name,
            League.country_id,
            Country.name
        ).join(
            Country, Country.id == League.country_id
        ).filter(
            League.id == league_id
        )
        result = await session.execute(query)
        try:
            result = result.one()
        except NoResultFound:
            raise Missing(f"лига с id - {league_id} не найдена")

    return to_one_league_schema(result)


def to_one_league_schema(league: tuple) -> LeagueSchema:
    return LeagueSchema(
        id=league[0],
        name=league[1],
        country=CountrySchema(id=league[2], name=league[3])
    )


async def get_seasons(league_id: int) -> list[SeasonSchema]:
    async with async_session() as session:
        query = select(
            Season.id,
            Season.name
        ).filter(
            Season.league_id == league_id
        )
        result = await session.execute(query)
        result = result.all()
        if len(result) == 0:
            raise Missing(f"сезонов с id лиги - {league_id} не найдено")

    return to_many_seasons_schemas(result)


def to_many_seasons_schemas(rows: list[tuple]) -> list[SeasonSchema]:
    result = []
    for season_id, name in rows:
        result.append(SeasonSchema(
            id=season_id,
            name=name,
            leader_id=0,
            leader_name="mock_team"
        ))

    return result


async def get_season(league_id: int, season_id: int) -> SeasonSchema | None:
    async with async_session() as session:
        query = select(
            Season.id,
            Season.name
        ).filter(
            and_(
                Season.league_id == league_id,
                Season.id == season_id
            )
        )
        result = await session.execute(query)
        try:
            result = result.one()
        except NoResultFound:
            raise Missing(f"сезонa с id лиги - {league_id} и id сезона - {season_id} не найдено")

    return to_one_season_schema(result)


def to_one_season_schema(season: tuple) -> SeasonSchema:
    return SeasonSchema(
        id=season[0],
        name=season[1],
        leader_id=0,
        leader_name="mock_team"
    )
