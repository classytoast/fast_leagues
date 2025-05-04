from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload, joinedload

from database import async_session
from errors import Missing
from models.db.persons import Manager, Player
from models.db.teams import Team
from models.pydantic.leagues import CountrySchema, SeasonSchema
from models.pydantic.persons import BasePersonSchema, BasePlayerSchema
from models.pydantic.teams import TeamRelSchema, TeamDetailsSchema


async def get_all_teams() -> list[TeamDetailsSchema]:
    """Выгрузить из БД список всех команд с краткой информацией"""
    async with async_session() as session:
        query = select(
            Team
        ).options(
            joinedload(Team.manager).joinedload(Manager.person)
        )
        result = await session.execute(query)
        result = result.scalars().all()

    return to_many_teams_schemas(result)


def to_many_teams_schemas(
        teams: list[Team]
) -> list[TeamDetailsSchema]:
    """Преобразует сырые SQL-результаты в список pydantic схем всех команд"""
    result = []
    for team in teams:
        if team.manager is not None:
            manager = BasePersonSchema(id=team.manager.id, name=team.manager.person.name)
        else:
            manager = None

        result.append(TeamDetailsSchema(
            id=team.id,
            name=team.name,
            founded=team.founded,
            manager=manager
        ))

    return result


async def get_one_team(team_id: int) -> TeamRelSchema:
    """Выгрузить из БД полную информацию о конкретной команде по ID"""
    async with async_session() as session:
        query = select(
            Team
        ).options(
            joinedload(Team.country)
        ).options(
            selectinload(Team.seasons)
        ).options(
            joinedload(Team.manager).joinedload(Manager.person)
        ).options(
            selectinload(Team.players).joinedload(Player.person)
        ).filter(
            Team.id == team_id
        )
        result = await session.execute(query)
        try:
            result = result.scalars().one()
        except NoResultFound:
            raise Missing(f"команда с id - {team_id} не найдена")

    return to_one_team_schema(result)


def to_one_team_schema(
        team: Team
) -> TeamRelSchema:
    """Преобразует сырые SQL-результаты в pydantic схему команды"""
    if team.manager is not None:
        manager = BasePersonSchema(id=team.manager.id, name=team.manager.person.name)
    else:
        manager = None

    team_schema = TeamRelSchema(
        id=team.id,
        name=team.name,
        founded=team.founded,
        manager=manager,
        country=CountrySchema(id=team.country.id, name=team.country.name),
        seasons=[SeasonSchema.model_validate(s, from_attributes=True) for s in team.seasons],
        players=[BasePlayerSchema(id=p.id, name=p.person.name, team_number=p.team_number) for p in team.players]
    )

    return team_schema
