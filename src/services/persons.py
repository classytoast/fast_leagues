from models.pydantic.persons import PlayerDetailsSchema, PersonDetailsSchema
from repositories import persons as data


async def get_player(player_id: int) -> PlayerDetailsSchema:
    """Получает полную информацию о конкретном игроке по его ID"""
    player = await data.get_player(player_id)
    return player


async def get_manager(manager_id: int) -> PersonDetailsSchema:
    """Получает полную информацию о конкретном тренере по его ID"""
    manager = await data.get_manager(manager_id)
    return manager
