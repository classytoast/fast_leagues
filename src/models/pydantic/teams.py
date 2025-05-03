from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from models.pydantic.leagues import CountrySchema, SeasonSchema
    from models.pydantic.persons import BasePersonSchema


class BaseTeamSchema(BaseModel):
    id: int
    name: str


class TeamSchema(BaseTeamSchema):
    founded: str
    manager: "BasePersonSchema"


class TeamRelSchema(TeamSchema):
    country: "CountrySchema"
    current_seasons: list['SeasonSchema'] = Field(validation_alias="seasons")


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
