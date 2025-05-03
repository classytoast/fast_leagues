from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field


if TYPE_CHECKING:
    from models.pydantic.leagues import CountrySchema
    from models.pydantic.teams import BaseTeamSchema


class BasePersonSchema(BaseModel):
    id: int
    name: str


class PersonSchema(BasePersonSchema):
    complete_name: str
    birth_date: datetime
    country: 'CountrySchema'
    team: Optional['BaseTeamSchema']


class StatusInGame(Enum):
    starting_lineups = 'starting lineups'
    substitutes = 'substitutes'


class PlayerInGameSchema(BasePersonSchema):
    team_number: int = Field(ge=1, description="Номер игрока должен быть ≥ 1")
    status = StatusInGame


class PlayerSchema(PersonSchema):
    team_number: int = Field(ge=1, description="Номер игрока должен быть ≥ 1")


class PlayerInTopTableSchema(BasePersonSchema):
    team: 'BaseTeamSchema'
    games: int
    effective_actions: int
