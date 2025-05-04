from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from models.pydantic.leagues import CountrySchema, SeasonSchema
    from models.pydantic.persons import BasePersonSchema, BasePlayerSchema


class BaseTeamSchema(BaseModel):
    id: int
    name: str


class TeamDetailsSchema(BaseTeamSchema):
    founded: str
    manager: Optional["BasePersonSchema"]


class TeamRelSchema(TeamDetailsSchema):
    country: "CountrySchema"
    current_seasons: list['SeasonSchema'] = Field(validation_alias="seasons")
    players: list["BasePlayerSchema"]


class TeamInSeasonSchema(BaseModel):
    team_id: int
    team_name: str
    position: int
    games: int
    wins: int
    draws: int
    loses: int
    scored_goals: int
    conceded_goals: int
    points: int
