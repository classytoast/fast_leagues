from datetime import datetime
from unittest.mock import patch

import pytest
from httpx import AsyncClient, ASGITransport

from errors import Missing
from main import app
from models.pydantic.games import (
    GameWithLeagueSchema,
    GameDetailSchema, GameEventSchema
)
from models.pydantic.leagues import SeasonSchema, LeagueSchema
from models.pydantic.persons import (
    BasePersonSchema,
    PlayerInGameSchema
)
from models.pydantic.teams import BaseTeamSchema


@pytest.mark.asyncio
@patch("api.games.service.get_game")
async def test_get_game(mock_service_get_game):
    service_get_player_return_value = GameDetailSchema(
        id=1,
        season=SeasonSchema(id=1, name='season1'),
        game_date=datetime(2025, 1, 1),
        home_team=BaseTeamSchema(id=1, name='team1'),
        guest_team=BaseTeamSchema(id=2, name='team2'),
        home_scored=2,
        guest_scored=1,
        home_team_composition=[
            PlayerInGameSchema(id=1, name='player1', status="starting lineups"),
            PlayerInGameSchema(id=2, name='player2', status="starting lineups"),
        ],
        guest_team_composition=[
            PlayerInGameSchema(id=3, name='player3', status="starting lineups"),
            PlayerInGameSchema(id=4, name='player4', status="starting lineups"),
        ],
        home_manager=BasePersonSchema(id=1, name='manager1'),
        guest_manager=None,
        game_events=[
            GameEventSchema(event_type='goal', minute='20', person=BasePersonSchema(id=1, name='player1')),
            GameEventSchema(event_type='goal', minute='75', person=BasePersonSchema(id=3, name='player3'))
        ]
    )
    mock_service_get_game.return_value = service_get_player_return_value

    expected_response = dict(
        id=1,
        season=dict(id=1, name='season1'),
        game_date='2025-01-01T00:00:00',
        home_team=dict(id=1, name='team1'),
        guest_team=dict(id=2, name='team2'),
        home_scored=2,
        guest_scored=1,
        home_team_composition=[
            dict(id=1, name='player1', status="starting lineups", team_number=None),
            dict(id=2, name='player2', status="starting lineups", team_number=None),
        ],
        guest_team_composition=[
            dict(id=3, name='player3', status="starting lineups", team_number=None),
            dict(id=4, name='player4', status="starting lineups", team_number=None),
        ],
        home_manager=dict(id=1, name='manager1'),
        guest_manager=None,
        game_events=[
            dict(event_type='goal', minute='20', person=dict(id=1, name='player1')),
            dict(event_type='goal', minute='75', person=dict(id=3, name='player3'))
        ]
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/games/1")

    assert response.json() == expected_response
    mock_service_get_game.assert_called_once_with(1)


@pytest.mark.asyncio
@patch("api.games.service.get_game")
async def test_get_game_missing(mock_service_get_game):
    mock_service_get_game.side_effect = Missing("Game not found")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/games/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}
    mock_service_get_game.assert_called_once_with(999)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "service_return, expected_response",
    [
        (
            [
                GameWithLeagueSchema(
                    id=1,
                    season=SeasonSchema(id=1, name='season1'),
                    league=LeagueSchema(id=1, name='league1'),
                    game_date=datetime(2025, 1, 1),
                    home_team=BaseTeamSchema(id=1, name='team1'),
                    guest_team=BaseTeamSchema(id=2, name='team2'),
                    home_scored=2,
                    guest_scored=1
                ),
                GameWithLeagueSchema(
                    id=2,
                    season=SeasonSchema(id=2, name='season2'),
                    league=LeagueSchema(id=2, name='league2'),
                    game_date=datetime(2025, 1, 1),
                    home_team=BaseTeamSchema(id=3, name='team3'),
                    guest_team=BaseTeamSchema(id=4, name='team4'),
                    home_scored=0,
                    guest_scored=0
                ),
            ],
            [
                dict(
                    id=1,
                    season=dict(id=1, name='season1'),
                    league=dict(id=1, name='league1'),
                    game_date='2025-01-01T00:00:00',
                    home_team=dict(id=1, name='team1'),
                    guest_team=dict(id=2, name='team2'),
                    home_scored=2,
                    guest_scored=1
                ),
                dict(
                    id=2,
                    season=dict(id=2, name='season2'),
                    league=dict(id=2, name='league2'),
                    game_date='2025-01-01T00:00:00',
                    home_team=dict(id=3, name='team3'),
                    guest_team=dict(id=4, name='team4'),
                    home_scored=0,
                    guest_scored=0
                ),
            ]
        ),

        ([], [])
    ]
)
@pytest.mark.asyncio
@patch("api.games.service.get_games_for_date")
async def test_get_games_for_date(mock_service_get_games, service_return, expected_response):
    service_get_manager_return_value = service_return
    mock_service_get_games.return_value = service_get_manager_return_value

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/games/?date=2025-01-01")

    assert response.json() == expected_response
    mock_service_get_games.assert_called_once()
