from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from models.pydantic.leagues import (
        SeasonSchema,
        LeagueSchema
    )
    from models.pydantic.teams import BaseTeamSchema
    from models.pydantic.persons import (
        PlayerInGameSchema,
        BasePersonSchema
    )


class BaseGameSchema(BaseModel):
    id: int
    season: 'SeasonSchema'
    game_date: Optional[datetime]
    home_team: 'BaseTeamSchema'
    guest_team: 'BaseTeamSchema'
    home_scored: int = Optional[Field(ge=0)]
    guest_scored: int = Optional[Field(ge=0)]


class GameWithLeagueSchema(BaseGameSchema):
    league: 'LeagueSchema'


class EventType(str, Enum):
    goal = 'goal'
    own_goal = 'own_goal'
    assist = 'assist'
    penalty_goal = 'penalty_goal'
    unrealized_penalty_goal = 'unrealized_penalty_goal'
    yellow_card = 'yellow_card'
    red_card = 'red_card'


class GameEventSchema(BaseModel):
    event_type: EventType
    minute: str
    person: 'BasePersonSchema'


class GameDetailSchema(BaseGameSchema):
    home_team_composition: list['PlayerInGameSchema']
    guest_team_composition: list['PlayerInGameSchema']
    home_manager: Optional['BasePersonSchema']
    guest_manager: Optional['BasePersonSchema']
    game_events: list['GameEventSchema']
