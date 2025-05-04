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


class PersonDetailsSchema(BasePersonSchema):
    full_name: str
    birth_date: datetime
    country: 'CountrySchema'
    team: Optional['BaseTeamSchema']


class BasePlayerSchema(BasePersonSchema):
    team_number: int = Field(ge=1)


class PlayerDetailsSchema(PersonDetailsSchema):
    team_number: Optional[int] = Field(ge=1)


class StatusInGame(str, Enum):
    starting_lineups = 'starting lineups'
    substitutes = 'substitutes'


class PlayerInGameSchema(BasePlayerSchema):
    status: StatusInGame


class PlayerStatsSummarySchema(BasePlayerSchema):
    team: 'BaseTeamSchema'
    games: int
    effective_actions: int

