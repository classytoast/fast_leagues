from models.pydantic.leagues import CountrySchema, SeasonSchema, SeasonWithLeaderSchema, SeasonRelSchema
from models.pydantic.persons import BasePersonSchema, BasePlayerSchema
from models.pydantic.teams import TeamRelSchema, BaseTeamSchema, TeamInSeasonSchema


BaseTeamSchema.model_rebuild()
TeamRelSchema.model_rebuild()
TeamInSeasonSchema.model_rebuild()
CountrySchema.model_rebuild()
SeasonSchema.model_rebuild()
SeasonWithLeaderSchema.model_rebuild()
SeasonRelSchema.model_rebuild()
BasePersonSchema.model_rebuild()
BasePlayerSchema.model_rebuild()
