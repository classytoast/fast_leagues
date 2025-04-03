from fastapi import APIRouter

from models.pydantic.leagues import LeagueSchema, SeasonSchema

router = APIRouter(prefix="/leagues")

league_list = [
        LeagueSchema(id=1, name='APL'),
        LeagueSchema(id=2, name='Bundesliga'),
        LeagueSchema(id=3, name='Seria A'),
]

season_list = [
        SeasonSchema(id=1, name='2024/2025', league=league_list[0], leader_id=23, leader_name='team1'),
        SeasonSchema(id=2, name='2024/2025', league=league_list[1], leader_id=10, leader_name='team2'),
        SeasonSchema(id=3, name='2024/2025', league=league_list[2], leader_id=69, leader_name='team3'),
]

#league_list[0].current_season = season_list[0]
#[1].current_season = season_list[1]
#league_list[2].current_season = season_list[2]


@router.get("/")
async def get_all_leagues() -> list[LeagueSchema]:
    return league_list


@router.get("/{league_id}")
async def get_one_league(league_id: str) -> LeagueSchema | None:
    return [l for l in league_list if l.id == int(league_id)][0]


@router.get("/{league_id}/seasons")
async def get_seasons(league_id: str) -> list[SeasonSchema]:
    return [s for s in season_list if s.league.id == int(league_id)]


@router.get("/{league_id}/seasons/{season_id}")
async def get_season(league_id: str, season_id: str) -> SeasonSchema | None:
    return [s for s in season_list if s.league.id == int(season_id)][0]
