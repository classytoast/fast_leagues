from typing import TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from models.pydantic.leagues import LeagueSchema


class TeamSchema(BaseModel):
    id: int
    name: str
    founded: str
    manager: str
    leagues: list['LeagueSchema']
