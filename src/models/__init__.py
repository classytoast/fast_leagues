from models.pydantic.games import (
    GameEventSchema,
    GameDetailSchema,
    BaseGameSchema,
    GameWithSeasonSchema
)
from models.pydantic.leagues import (
    CountrySchema,
    SeasonSchema,
    SeasonWithLeaderSchema,
    SeasonRelSchema,
    SeasonWithPlayersSchema,
    SeasonWithTopPlayersSchema,
    SeasonWithGamesSchema
)
from models.pydantic.persons import (
    BasePersonSchema,
    BasePlayerSchema,
    PlayerDetailsSchema,
    PersonDetailsSchema, PlayerInGameSchema,
    PlayerStatsSummarySchema
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
SeasonWithTopPlayersSchema.model_rebuild()
SeasonWithGamesSchema.model_rebuild()
SeasonRelSchema.model_rebuild()
BasePersonSchema.model_rebuild()
BasePlayerSchema.model_rebuild()
PlayerDetailsSchema.model_rebuild()
PlayerInGameSchema.model_rebuild()
SeasonWithPlayersSchema.model_rebuild()
PersonDetailsSchema.model_rebuild()
PlayerStatsSummarySchema.model_rebuild()
BaseGameSchema.model_rebuild()
GameEventSchema.model_rebuild()
GameDetailSchema.model_rebuild()
GameWithSeasonSchema.model_rebuild()
