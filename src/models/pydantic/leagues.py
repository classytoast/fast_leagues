from typing import Optional

from pydantic import BaseModel


class LeagueSchema(BaseModel):
    id: int
    name: str
    current_season: Optional['SeasonSchema'] = None


class SeasonSchema(BaseModel):
    id: int
    name: str
    league: Optional[LeagueSchema] = None
    leader_id: int
    leader_name: str

