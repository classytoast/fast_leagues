from models.pydantic.leagues import CountrySchema, SeasonSchema, SeasonWithLeaderSchema, SeasonRelSchema
from models.pydantic.teams import TeamRelSchema, TeamSchema, TeamInSeasonSchema


TeamSchema.model_rebuild()
TeamRelSchema.model_rebuild()
TeamInSeasonSchema.model_rebuild()
CountrySchema.model_rebuild()
SeasonSchema.model_rebuild()
SeasonWithLeaderSchema.model_rebuild()
SeasonRelSchema.model_rebuild()
