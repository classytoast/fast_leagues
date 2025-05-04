from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from models.pydantic.teams import BaseTeamSchema, TeamInSeasonSchema
    from models.pydantic.persons import PlayerDetailsSchema


class CountrySchema(BaseModel):
    id: int
    name: str


class LeagueSchema(BaseModel):
    id: int
    name: str


class LeagueCountrySchema(LeagueSchema):
    country: 'CountrySchema'


class LeagueWithCurrentSeasonSchema(LeagueCountrySchema):
    current_season: 'SeasonWithLeaderSchema' = Field(validation_alias="seasons")


class LeagueRelSchema(LeagueCountrySchema):
    seasons: list['SeasonSchema']


class SeasonSchema(BaseModel):
    id: int
    name: str


class SeasonWithLeaderSchema(SeasonSchema):
    leader: 'BaseTeamSchema' = Field(validation_alias="teams")


class SeasonWithPlayersSchema(SeasonSchema):
    players: list['PlayerDetailsSchema']


class SeasonRelSchema(SeasonSchema):
    league: 'LeagueCountrySchema'
    teams: list['TeamInSeasonSchema']
