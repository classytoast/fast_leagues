import bisect

from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import async_session
from errors import Missing
from models.db.games import Game
from models.db.leagues import League, Country, Season
from models.db.persons import Player, Person
from models.db.teams import SeasonTeam, Team
from models.mongo_documents.games import GameDocument
from models.pydantic.games import BaseGameSchema
from models.pydantic.leagues import (
    CountrySchema,
    LeagueWithCurrentSeasonSchema,
    SeasonWithLeaderSchema,
    LeagueCountrySchema,
    SeasonRelSchema,
    SeasonWithPlayersSchema,
    SeasonWithTopPlayersSchema,
    SeasonWithGamesSchema
)
from models.pydantic.persons import (
    PlayerDetailsSchema,
    PlayerStatsSummarySchema
)
from models.pydantic.teams import (
    TeamInSeasonSchema,
    BaseTeamSchema
)


async def get_all_leagues() -> list[LeagueWithCurrentSeasonSchema]:
    """Выгрузить из БД список всех лиг с их текущими сезонами и лидирующими командами"""
    async with async_session() as session:
        query = select(
            League.id,
            League.name,
            Country.id,
            Country.name,
            Season.id,
            Season.name,
            Team.id,
            Team.name
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
    """Преобразует сырые SQL-результаты в список pydantic схем лиг с текущими сезонами"""
    result = []
    for row in rows:
        (league_id, league_name, country_id, country_name,
         season_id, season_name, leader_id, leader_name) = row

        result.append(LeagueWithCurrentSeasonSchema(
            id=league_id,
            name=league_name,
            country=CountrySchema(id=country_id, name=country_name),
            seasons=SeasonWithLeaderSchema(
                id=season_id,
                name=season_name,
                teams=BaseTeamSchema(
                    id=leader_id,
                    name=leader_name
                ))
        ))

    return result


async def get_one_league(league_id: int) -> LeagueCountrySchema:
    """Выгрузить из БД подробную информацию о конкретной лиге с данными о стране"""
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
    """Преобразует кортеж данных лиги в pydantic схему"""
    return LeagueCountrySchema(
        id=league[0],
        name=league[1],
        country=CountrySchema(id=league[2], name=league[3])
    )


async def get_seasons(league_id: int) -> list[SeasonWithLeaderSchema]:
    """Выгрузить из БД список сезонов указанной лиги с командами-лидерами"""
    async with async_session() as session:
        query = select(
            Season.id,
            Season.name,
            Team.id,
            Team.name
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
    """Преобразует сырые данные сезонов в список pydantic схем"""
    result = []
    for season_id, season_name, leader_id, leader_name in rows:
        result.append(SeasonWithLeaderSchema(
            id=season_id,
            name=season_name,
            teams=BaseTeamSchema(
                id=leader_id,
                name=leader_name
            )
        ))

    return result


async def get_season(league_id: int, season_id: int) -> SeasonRelSchema:
    """Выгрузить из БД полную информацию о конкретном сезоне лиги.

    SQL-логика:
        Выполняет два запроса:
        1. Основные данные сезона, лиги и страны
        2. Данные всех команд в сезоне с их статистикой
    """
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
    """Собирает полную pydantic схему сезона с данными о командах"""
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


async def get_players_in_season(league_id: int, season_id: int) -> SeasonWithPlayersSchema:
    """Выгрузить из БД информацию об игроках в конкретном сезоне лиги"""
    async with async_session() as session:
        query = select(
            Season
        ).options(
            selectinload(
                Season.teams
            ).selectinload(
                Team.players
            ).joinedload(
                Player.person
            ).joinedload(
                Person.country
            )
        ).filter(
            and_(
                Season.league_id == league_id,
                Season.id == season_id
            )
        )

        result = await session.execute(query)
        try:
            season_result = result.scalars().one()
        except NoResultFound:
            raise Missing(f"сезонa с id лиги - {league_id} и id сезона - {season_id} не найдено")

    return to_season_with_players_schema(season_result)


def to_season_with_players_schema(season_data: Season) -> SeasonWithPlayersSchema:
    """Собирает pydantic схему сезона с данными об игроках"""
    players = []
    for team in season_data.teams:
        for player in team.players:
            players.append(PlayerDetailsSchema(
                id=player.id,
                name=player.person.name,
                full_name=player.person.full_name,
                birth_date=player.person.birth_date,
                team_number=player.team_number,
                country=CountrySchema.model_validate(player.person.country, from_attributes=True),
                team=BaseTeamSchema.model_validate(team, from_attributes=True)
            ))

    return SeasonWithPlayersSchema(
        id=season_data.id,
        name=season_data.name,
        players=players
    )


async def get_games_for_season(league_id: int, season_id: int) -> SeasonWithGamesSchema:
    """Выгрузить из БД информацию об матчах в конкретном сезоне лиги"""
    async with async_session() as session:
        query = select(
            Season
        ).outerjoin(
            Game
        ).options(
            selectinload(
                Season.games
            ).joinedload(
                Game.home_team
            ),
            selectinload(
                Season.games
            ).joinedload(
                Game.guest_team
            )
        ).filter(
            and_(
                Season.league_id == league_id,
                Season.id == season_id
            )
        ).order_by(
            Game.game_date
        )

        result = await session.execute(query)
        try:
            season_result = result.unique().scalars().one()
        except NoResultFound:
            raise Missing(f"сезонa с id лиги - {league_id} и id сезона - {season_id} не найдено")

    return SeasonWithGamesSchema.model_validate(season_result, from_attributes=True)


async def get_scores_in_season(league_id: int, season_id: int) -> SeasonWithTopPlayersSchema:
    """Выгрузить из БД информацию о бомбардирах в конкретном сезоне лиги"""
    async with async_session() as session:
        base_season = await get_base_season(session, league_id, season_id)

        games_for_players = await get_number_of_games_for_players_in_season(season_id)

        top_scores = await get_top_scores_in_season(season_id)

    return to_season_with_top_players_schema(
        base_season,
        games_for_players,
        top_scores,
        'goals'
    )


async def get_base_season(
        session: AsyncSession,
        league_id: int,
        season_id: int
) -> Season:
    """Выгрузить базовые данные из бд о конкретном сезоне"""
    query = select(
        Season
    ).filter(
        and_(
            Season.league_id == league_id,
            Season.id == season_id
        )
    )
    result = await session.execute(query)
    try:
        season_result = result.scalars().one()
    except NoResultFound:
        raise Missing(f"сезонa с id лиги - {league_id} и id сезона - {season_id} не найдено")

    return season_result


async def get_number_of_games_for_players_in_season(
        season_id: int
) -> list[dict[str, dict[str, str | int] | int]]:
    """Выгрузить данные из mongodb о количестве матчей для каждого игрока в сезоне"""
    pipeline = [
        {"$match": {"season_id": season_id}},

        {"$project": {
            "players": {
                "$concatArrays": ["$home_start_composition", "$guest_start_composition"]
            }
        }},

        {"$unwind": "$players"},

        {"$group": {
            "_id": {"player_id": "$players.id", "player_name": "$players.name",
                    "team_id": "$players.team.id", "team_name": "$players.team.name"},
            "games": {"$sum": 1}
        }},

        {"$sort": {"_id.player_id": 1}}
    ]

    return await GameDocument.aggregate(pipeline).to_list()


async def get_top_scores_in_season(
        season_id: int
) -> list[dict[str, dict[str, str | int] | int]]:
    """Выгрузить данные из mongodb о лучших бомбардирах в сезоне"""
    pipeline = [
        {"$match": {"season_id": season_id}},

        {"$unwind": "$events"},

        {"$match": {
            "events.event_type": {"$in": ["goal", "penalty_goal"]}
        }},

        {"$group": {
            "_id": {"player_id": "$events.person.id", "player_name": "$events.person.name",
                    "team_id": "$events.person.team.id", "team_name": "$events.person.team.name"},
            "goals": {"$sum": 1}
        }},

        {"$sort": {"_id.player_id": 1}}
    ]

    return await GameDocument.aggregate(pipeline).to_list()


def to_season_with_top_players_schema(
        season_data: Season,
        players_with_games: list[dict[str, dict[str, str | int] | int]],
        top_players: list[dict[str, dict[str, str | int] | int]],
        event_type: str
) -> SeasonWithTopPlayersSchema:
    """Собирает pydantic схему сезона о лучших игроках по конкретному показателю"""
    players = []
    for player in players_with_games:
        idx_player_with_actions = bisect.bisect_left(
            top_players,
            player['_id']['player_id'],
            key=lambda x: x['_id']['player_id']
        )
        try:
            effective_actions = top_players[idx_player_with_actions][event_type]
        except IndexError:
            effective_actions = 0

        players.append(PlayerStatsSummarySchema(
            id=player['_id']['player_id'],
            name=player['_id']['player_name'],
            team_number=None,
            team=BaseTeamSchema(id=player['_id']['team_id'], name=player['_id']['team_name']),
            games=player['games'],
            effective_actions=effective_actions
        ))

    players.sort(key=lambda x: (-x.effective_actions, x.games, x.name))

    return SeasonWithTopPlayersSchema(
        id=season_data.id,
        name=season_data.name,
        players=players
    )
