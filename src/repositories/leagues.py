from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from database import async_session
from errors import Missing
from models.db.leagues import League, Country, Season
from models.db.teams import SeasonTeam, Team
from models.pydantic.leagues import (
    CountrySchema,
    LeagueWithCurrentSeasonSchema,
    SeasonWithLeaderSchema,
    LeagueCountrySchema, SeasonRelSchema
)
from models.pydantic.teams import TeamSchema, TeamInSeasonSchema


async def get_all_leagues() -> list[LeagueWithCurrentSeasonSchema]:
    async with async_session() as session:
        query = select(
            League.id,
            League.name,
            Country.id,
            Country.name,
            Season.id,
            Season.name,
            Team.id,
            Team.name,
            Team.founded,
            Team.manager
        ).select_from(
            League
        ).join(
            Country, Country.id == League.country_id
        ).join(
            Season, League.id == Season.league_id
        ).join(
            SeasonTeam, Season.id == SeasonTeam.season_id
        ).join(
            Team, Team.id == SeasonTeam.team_id
        ).filter(
            and_(
                Season.is_current_season == True,
                SeasonTeam.position == 1
            )
        )
        result = await session.execute(query)
        result = result.all()

    return to_many_leagues_schemas(result)


def to_many_leagues_schemas(
        rows: list[tuple]
) -> list[LeagueWithCurrentSeasonSchema]:
    result = []
    for row in rows:
        (league_id, league_name, country_id, country_name,
         season_id, season_name, leader_id, leader_name, leader_founded, leader_manager) = row

        result.append(LeagueWithCurrentSeasonSchema(
            id=league_id,
            name=league_name,
            country=CountrySchema(id=country_id, name=country_name),
            seasons=SeasonWithLeaderSchema(
                id=season_id,
                name=season_name,
                teams=TeamSchema(
                    id=leader_id,
                    name=leader_name,
                    founded=leader_founded,
                    manager=leader_manager
                ))
        ))

    return result


async def get_one_league(league_id: int) -> LeagueCountrySchema:
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


def to_one_league_schema(league: tuple) -> LeagueCountrySchema:
    return LeagueCountrySchema(
        id=league[0],
        name=league[1],
        country=CountrySchema(id=league[2], name=league[3])
    )


async def get_seasons(league_id: int) -> list[SeasonWithLeaderSchema]:
    async with async_session() as session:
        query = select(
            Season.id,
            Season.name,
            Team.id,
            Team.name,
            Team.founded,
            Team.manager
        ).join(
            SeasonTeam, Season.id == SeasonTeam.season_id
        ).join(
            Team, Team.id == SeasonTeam.team_id
        ).filter(
            and_(
                Season.league_id == league_id,
                SeasonTeam.position == 1
            )
        )
        result = await session.execute(query)
        result = result.all()
        if len(result) == 0:
            raise Missing(f"сезонов с id лиги - {league_id} не найдено")

    return to_many_seasons_schemas(result)


def to_many_seasons_schemas(rows: list[tuple]) -> list[SeasonWithLeaderSchema]:
    result = []
    for season_id, season_name, leader_id, leader_name, leader_founded, leader_manager in rows:
        result.append(SeasonWithLeaderSchema(
            id=season_id,
            name=season_name,
            teams=TeamSchema(
                id=leader_id,
                name=leader_name,
                founded=leader_founded,
                manager=leader_manager
            )
        ))

    return result


async def get_season(league_id: int, season_id: int) -> SeasonRelSchema:
    async with async_session() as session:
        query = select(
            Season.id,
            Season.name,
            League.id,
            League.name,
            Country.id,
            Country.name
        ).join(
            League, League.id == Season.league_id
        ).join(
            Country, Country.id == League.country_id
        ).filter(
            and_(
                Season.league_id == league_id,
                Season.id == season_id
            )
        )
        season_result = await session.execute(query)
        try:
            season_data = season_result.one()
        except NoResultFound:
            raise Missing(f"сезонa с id лиги - {league_id} и id сезона - {season_id} не найдено")

        query = select(
            Team.id,
            Team.name,
            SeasonTeam.position,
            SeasonTeam.games,
            SeasonTeam.wins,
            SeasonTeam.draws,
            SeasonTeam.loses,
            SeasonTeam.scored_goals,
            SeasonTeam.conceded_goals,
            SeasonTeam.points
        ).join(
            Team, Team.id == SeasonTeam.team_id
        ).filter(
            SeasonTeam.season_id == season_id
        ).order_by(
            SeasonTeam.position
        )
        teams_result = await session.execute(query)
        teams_data = teams_result.all()

    return to_one_season_schema(season_data, teams_data)


def to_one_season_schema(season: tuple, teams: list[tuple]) -> SeasonRelSchema:
    teams_schema = []
    for team in teams:
        team_id, name, position, games, wins, draws, loses, scored_goals, conceded_goals, points = team
        teams_schema.append(TeamInSeasonSchema(
            team_id=team_id,
            team_name=name,
            position=position,
            games=games,
            wins=wins,
            draws=draws,
            loses=loses,
            scored_goals=scored_goals,
            conceded_goals=conceded_goals,
            points=points
        ))

    season_id, season_name, league_id, league_name, country_id, country_name = season
    return SeasonRelSchema(
        id=season_id,
        name=season_name,
        league=LeagueCountrySchema(
            id=league_id,
            name=league_name,
            country=CountrySchema(id=country_id, name=country_name)
        ),
        teams=teams_schema
    )
