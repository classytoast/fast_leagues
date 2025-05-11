from models.pydantic.games import GameEventSchema, GameDetailSchema
from models.pydantic.leagues import (
    CountrySchema,
    SeasonSchema,
    SeasonWithLeaderSchema,
    SeasonRelSchema,
    SeasonWithPlayersSchema
)
from models.pydantic.persons import (
    BasePersonSchema,
    BasePlayerSchema,
    PlayerDetailsSchema,
    PersonDetailsSchema, PlayerInGameSchema
)
from models.pydantic.teams import (
    TeamRelSchema,
    BaseTeamSchema,
    TeamInSeasonSchema,
    TeamDetailsSchema
)


BaseTeamSchema.model_rebuild()
TeamRelSchema.model_rebuild()
TeamInSeasonSchema.model_rebuild()
TeamDetailsSchema.model_rebuild()
CountrySchema.model_rebuild()
SeasonSchema.model_rebuild()
SeasonWithLeaderSchema.model_rebuild()
SeasonRelSchema.model_rebuild()
BasePersonSchema.model_rebuild()
BasePlayerSchema.model_rebuild()
PlayerDetailsSchema.model_rebuild()
PlayerInGameSchema.model_rebuild()
SeasonWithPlayersSchema.model_rebuild()
PersonDetailsSchema.model_rebuild()
GameEventSchema.model_rebuild()
GameDetailSchema.model_rebuild()
