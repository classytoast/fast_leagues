from typing import Optional

from pydantic import BaseModel


class CountrySchema(BaseModel):
    id: int
    name: str

class LeagueSchema(BaseModel):
    id: int
    name: str
    country: 'CountrySchema'
    current_season: Optional['SeasonSchema'] = None


class SeasonSchema(BaseModel):
    id: int
    name: str
    league: Optional['LeagueSchema'] = None
    leader_id: int
    leader_name: str

