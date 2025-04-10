from models.pydantic.leagues import SeasonSchema, LeagueSchema


league_list = [
]

season_list = [
]

#league_list[0].current_season = season_list[0]
#[1].current_season = season_list[1]
#league_list[2].current_season = season_list[2]


async def get_all_leagues() -> list[LeagueSchema]:
    return league_list


async def get_one_league(league_id: int) -> LeagueSchema | None:
    return [l for l in league_list if l.id == league_id][0]


async def get_seasons(league_id: int) -> list[SeasonSchema]:
    return [s for s in season_list if s.league.id == league_id]


async def get_season(league_id: int, season_id: int) -> SeasonSchema | None:
    return [s for s in season_list if s.league.id == season_id][0]
