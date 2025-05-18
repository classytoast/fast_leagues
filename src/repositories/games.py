from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import async_session
from errors import Missing
from models.db.games import Game
from models.db.leagues import Season
from models.mongo_documents.games import GameDocument
from models.pydantic.games import (
    GameDetailSchema,
    GameEventSchema,
    GameWithLeagueSchema)
from models.pydantic.leagues import (
    SeasonSchema,
    LeagueSchema
)
from models.pydantic.persons import (
    PlayerInGameSchema,
    BasePersonSchema
)
from models.pydantic.teams import BaseTeamSchema


async def get_game(game_id: int) -> GameDetailSchema:
    """Выгрузить из БД подробную информацию о конкретном матче"""
    async with async_session() as session:
        game_from_postgresql = await _get_game_from_postgresql(session, game_id)

        game_from_mongo = await _get_game_detail_from_mongo(game_id)

    return _to_one_game_schema(game_from_postgresql, game_from_mongo)


async def _get_game_from_postgresql(
        session: AsyncSession,
        game_id: int
) -> Game:
    """Выгрузить из postgresql информацию о конкретном матче"""
    query = select(
        Game
    ).options(
        joinedload(Game.season)
    ).options(
        joinedload(Game.home_team)
    ).options(
        joinedload(Game.guest_team)
    ).filter(
        Game.id == game_id
    )
    result = await session.execute(query)
    try:
        result = result.scalars().one()
    except NoResultFound:
        raise Missing(f"матча с id - {game_id} не найдено")

    return result


async def _get_game_detail_from_mongo(
        game_id: int
) -> GameDocument:
    """Выгрузить из mongo подробную информацию о конкретном матче"""
    result = await GameDocument.find_one({"game_id": game_id})
    return result


def _to_one_game_schema(
        orm_game: Game,
        odm_game: GameDocument
) -> GameDetailSchema:
    """Преобразует данные матча из БД в pydantic схему"""
    home_start = [PlayerInGameSchema(id=x.id, name=x.name, status="starting lineups")
                  for x in odm_game.home_start_composition]
    home_substitution = [PlayerInGameSchema(id=x.id, name=x.name, status="substitutes")
                         for x in odm_game.home_substitution]
    guest_start = [PlayerInGameSchema(id=x.id, name=x.name, status="starting lineups")
                   for x in odm_game.guest_start_composition]
    guest_substitution = [PlayerInGameSchema(id=x.id, name=x.name, status="substitutes")
                          for x in odm_game.guest_substitution]

    if odm_game.home_manager is not None:
        home_manager = BasePersonSchema(id=odm_game.home_manager.id, name=odm_game.home_manager.name)
    else:
        home_manager = None

    if odm_game.guest_manager is not None:
        guest_manager = BasePersonSchema(id=odm_game.guest_manager.id, name=odm_game.guest_manager.name)
    else:
        guest_manager = None

    events = []
    for event in odm_game.events:
        events.append(GameEventSchema(
            event_type=event.event_type,
            minute=event.minute,
            person=BasePersonSchema(id=event.person.id, name=event.person.name)
        ))

    return GameDetailSchema(
        id=orm_game.id,
        season=SeasonSchema.model_validate(orm_game.season, from_attributes=True),
        game_date=orm_game.game_date,
        home_team=BaseTeamSchema.model_validate(orm_game.home_team, from_attributes=True),
        guest_team=BaseTeamSchema.model_validate(orm_game.guest_team, from_attributes=True),
        home_scored=orm_game.home_scored,
        guest_scored=orm_game.guest_scored,
        home_team_composition=home_start + home_substitution,
        guest_team_composition=guest_start + guest_substitution,
        home_manager=home_manager,
        guest_manager=guest_manager,
        game_events=events
    )


async def get_games_for_date(date: datetime) -> list[GameWithLeagueSchema]:
    """Выгрузить из БД все матчи за определенный день"""
    async with async_session() as session:
        query = select(
            Game
        ).options(
            joinedload(Game.season).joinedload(Season.league)
        ).options(
            joinedload(Game.home_team)
        ).options(
            joinedload(Game.guest_team)
        ).filter(
            Game.game_date == date
        )

        result = await session.execute(query)
        result = result.scalars().all()

    return to_games_for_date_schema(result)


def to_games_for_date_schema(
        games: list[Game]
) -> list[GameWithLeagueSchema]:
    """Преобразует список матчей из БД в pydantic схему"""
    games_schema = []

    for game in games:
        games_schema.append(GameWithLeagueSchema(
            id=game.id,
            season=SeasonSchema.model_validate(game.season, from_attributes=True),
            league=LeagueSchema.model_validate(game.season.league, from_attributes=True),
            game_date=game.game_date,
            home_team=BaseTeamSchema.model_validate(game.home_team, from_attributes=True),
            guest_team=BaseTeamSchema.model_validate(game.guest_team, from_attributes=True),
            home_scored=game.home_scored,
            guest_scored=game.guest_scored
        ))

    return games_schema
