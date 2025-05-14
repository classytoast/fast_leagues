from enum import Enum
from typing import Optional

from beanie import Document
from pydantic import BaseModel


class EventType(Enum):
    goal = 'goal'
    own_goal = 'own_goal'
    assist = 'assist'
    penalty_goal = 'penalty_goal'
    unrealized_penalty_goal = 'unrealized_penalty_goal'
    yellow_card = 'yellow_card'
    red_card = 'red_card'


class TeamEmbeddedObject(BaseModel):
    id: int
    name: str


class PersonEmbeddedObject(BaseModel):
    id: int
    name: str
    team: 'TeamEmbeddedObject'


class EventEmbeddedObject(BaseModel):
    event_type: EventType
    minute: str
    person: 'PersonEmbeddedObject'


class GameDocument(Document):
    game_id: int
    season_id: int
    league_id: int
    home_start_composition: list['PersonEmbeddedObject'] = []
    guest_start_composition: list['PersonEmbeddedObject'] = []
    home_substitution: list['PersonEmbeddedObject'] = []
    guest_substitution: list['PersonEmbeddedObject'] = []
    home_manager: Optional['PersonEmbeddedObject'] = None
    guest_manager: Optional['PersonEmbeddedObject'] = None
    events: list['EventEmbeddedObject'] = []

    class Settings:
        name = "games"
