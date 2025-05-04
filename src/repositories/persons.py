from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from database import async_session
from errors import Missing
from models.db.persons import Player, Person, Manager
from models.pydantic.leagues import CountrySchema
from models.pydantic.persons import PlayerDetailsSchema, PersonDetailsSchema
from models.pydantic.teams import BaseTeamSchema


async def get_player(player_id: int) -> PlayerDetailsSchema:
    """Выгрузить из БД полную информацию о конкретном игроке"""
    async with async_session() as session:
        query = select(
            Player
        ).options(
            joinedload(
                Player.person
            ).joinedload(
                Person.country
            )
        ).options(
            joinedload(Player.team)
        ).filter(
            Player.id == player_id
        )
        result = await session.execute(query)
        try:
            result = result.scalars().one()
        except NoResultFound:
            raise Missing(f"игрок с id - {player_id} не найден")

    return to_player_schema(result)


def to_player_schema(player: Player) -> PlayerDetailsSchema:
    """Преобразует сырой SQL-результат в pydantic схему игрока"""
    if player.team is not None:
        team = BaseTeamSchema.model_validate(player.team, from_attributes=True)
    else:
        team = None

    player_schema = PlayerDetailsSchema(
        id=player.id,
        name=player.person.name,
        full_name=player.person.full_name,
        birth_date=player.person.birth_date,
        team_number=player.team_number,
        country=CountrySchema.model_validate(player.person.country, from_attributes=True),
        team=team
    )

    return player_schema


async def get_manager(manager_id: int) -> PersonDetailsSchema:
    """Выгрузить из БД полную информацию о конкретном тренере"""
    async with async_session() as session:
        query = select(
            Manager
        ).options(
            joinedload(
                Manager.person
            ).joinedload(
                Person.country
            )
        ).options(
            joinedload(Manager.team)
        ).filter(
            Manager.id == manager_id
        )
        result = await session.execute(query)
        try:
            result = result.scalars().one()
        except NoResultFound:
            raise Missing(f"тренер с id - {manager_id} не найден")

    return to_manager_schema(result)


def to_manager_schema(manager: Manager) -> PersonDetailsSchema:
    """Преобразует сырой SQL-результат в pydantic схему тренера"""
    if manager.team is not None:
        team = BaseTeamSchema.model_validate(manager.team, from_attributes=True)
    else:
        team = None

    manager_schema = PersonDetailsSchema(
        id=manager.id,
        name=manager.person.name,
        full_name=manager.person.full_name,
        birth_date=manager.person.birth_date,
        country=CountrySchema.model_validate(manager.person.country, from_attributes=True),
        team=team
    )

    return manager_schema
