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


class PersonDocument(BaseModel):
    id: int
    name: str


class EventDocument(BaseModel):
    event_type: EventType
    minute: str
    person: 'PersonDocument'


class GameDocument(Document):
    game_id: int
    season_id: int
    league_id: int
    home_start_composition: list['PersonDocument'] = []
    guest_start_composition: list['PersonDocument'] = []
    home_substitution: list['PersonDocument'] = []
    guest_substitution: list['PersonDocument'] = []
    home_manager: Optional['PersonDocument'] = None
    guest_manager: Optional['PersonDocument'] = None
    events: list['EventDocument'] = []

    class Settings:
        name = "games"
