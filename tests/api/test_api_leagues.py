from datetime import datetime
from unittest.mock import patch

import pytest
from httpx import AsyncClient, ASGITransport

from errors import Missing
from main import app
from models.pydantic.leagues import (
    CountrySchema,
    LeagueWithCurrentSeasonSchema,
    SeasonWithLeaderSchema,
    LeagueCountrySchema,
    SeasonRelSchema, SeasonWithPlayersSchema,
    SeasonWithTopPlayersSchema
)
from models.pydantic.persons import (
    PlayerDetailsSchema,
    PlayerStatsSummarySchema
)
from models.pydantic.teams import (
    BaseTeamSchema,
    TeamInSeasonSchema
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "service_return",
    [
        [
            LeagueWithCurrentSeasonSchema(
                id=1,
                name='APL',
                country=CountrySchema(id=1, name='country1'),
                seasons=SeasonWithLeaderSchema(
                    id=1,
                    name='2024/2025',
                    teams=BaseTeamSchema(
                        id=1,
                        name='team1'
                    ))
            ),
            LeagueWithCurrentSeasonSchema(
                id=2,
                name='Bundesliga',
                country=CountrySchema(id=2, name='country2'),
                seasons=SeasonWithLeaderSchema(
                    id=2,
                    name='2024/2025',
                    teams=BaseTeamSchema(
                        id=15,
                        name='team2'
                    ))
            )
        ],
        []
    ]
)
@patch("api.leagues.service.get_all_leagues")
async def test_get_all_leagues(mock_service_get_all, service_return):
    mock_service_get_all.return_value = service_return

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/")

    assert response.json() == [m.model_dump() for m in service_return]
    mock_service_get_all.assert_called_once()


@pytest.mark.asyncio
@patch("api.leagues.service.get_one_league")
async def test_get_one_league(mock_service_get_one):
    service_get_one_return_value = LeagueCountrySchema(
        id=1,
        name='APL',
        country=CountrySchema(id=1, name='country1')
    )
    mock_service_get_one.return_value = service_get_one_return_value

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/1")

    assert response.json() == service_get_one_return_value.model_dump()
    mock_service_get_one.assert_called_once_with(1)


@pytest.mark.asyncio
@patch("api.leagues.service.get_one_league")
async def test_get_one_league_missing(mock_service_get_one):
    mock_service_get_one.side_effect = Missing("League not found")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "League not found"}
    mock_service_get_one.assert_called_once_with(999)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "service_return",
    [
        [
            SeasonWithLeaderSchema(
                id=1,
                name='2024/2025',
                teams=BaseTeamSchema(
                    id=1,
                    name='team1'
                )
            ),
            SeasonWithLeaderSchema(
                id=2,
                name='2024/2025',
                teams=BaseTeamSchema(
                    id=2,
                    name='team2'
                )
            )
        ],
        []
    ]
)
@patch("api.leagues.service.get_seasons")
async def test_get_seasons(mock_service_get_seasons, service_return):
    mock_service_get_seasons.return_value = service_return

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/1/seasons")

    assert response.json() == [m.model_dump() for m in service_return]
    mock_service_get_seasons.assert_called_once_with(1)


@pytest.mark.asyncio
@patch("api.leagues.service.get_seasons")
async def test_get_seasons_missing(mock_service_get_season):
    mock_service_get_season.side_effect = Missing("Seasons not found")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/999/seasons")

    assert response.status_code == 404
    assert response.json() == {"detail": "Seasons not found"}
    mock_service_get_season.assert_called_once_with(999)


@pytest.mark.asyncio
@patch("api.leagues.service.get_season")
async def test_get_season(mock_service_get_season):
    service_get_season_return_value = SeasonRelSchema(
            id=1,
            name='2024/2025',
            league=LeagueCountrySchema(id=1, name='APL', country=CountrySchema(id=1, name='country1')),
            teams=[
                TeamInSeasonSchema(
                    team_id=1,
                    team_name='team1',
                    position=1,
                    games=3,
                    wins=2,
                    draws=1,
                    loses=0,
                    scored_goals=5,
                    conceded_goals=2,
                    points=7
                ),
                TeamInSeasonSchema(
                    team_id=1,
                    team_name='team2',
                    position=2,
                    games=3,
                    wins=1,
                    draws=1,
                    loses=1,
                    scored_goals=3,
                    conceded_goals=1,
                    points=4
                )
            ]
    )
    mock_service_get_season.return_value = service_get_season_return_value

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/1/seasons/1")

    assert response.json() == service_get_season_return_value.model_dump()
    mock_service_get_season.assert_called_once_with(1, 1)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint, service_args",
    [
        ("/leagues/1/seasons/999", (1, 999)),
        ("/leagues/999/seasons/1", (999, 1)),
    ]
)
@patch("api.leagues.service.get_season")
async def test_get_season_missing(mock_service_get_season, endpoint, service_args):
    mock_service_get_season.side_effect = Missing("Season not found")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(endpoint)

    assert response.status_code == 404
    assert response.json() == {"detail": "Season not found"}
    mock_service_get_season.assert_called_once_with(*service_args)


@pytest.mark.asyncio
@patch("api.leagues.service.get_players_in_season")
async def test_get_players_in_season(mock_service_get_players):
    service_get_players_return_value = SeasonWithPlayersSchema(
            id=1,
            name='2024/2025',
            players=[
                PlayerDetailsSchema(
                    id=1,
                    name='player1',
                    full_name='full_player1',
                    birth_date=datetime(2000, 1, 1),
                    team_number=10,
                    country=CountrySchema(id=1, name='country1'),
                    team=BaseTeamSchema(id=1, name='team1')
                ),
                PlayerDetailsSchema(
                    id=2,
                    name='player2',
                    full_name='full_player2',
                    birth_date=datetime(2000, 2, 1),
                    team_number=20,
                    country=CountrySchema(id=2, name='country2'),
                    team=BaseTeamSchema(id=2, name='team2')
                )
            ]
    )
    mock_service_get_players.return_value = service_get_players_return_value

    expected_response = dict(
        id=1,
        name='2024/2025',
        players=[
            dict(
                id=1,
                name='player1',
                full_name='full_player1',
                birth_date='2000-01-01T00:00:00',
                team_number=10,
                country=dict(id=1, name='country1'),
                team=dict(id=1, name='team1')
            ),
            dict(
                id=2,
                name='player2',
                full_name='full_player2',
                birth_date='2000-02-01T00:00:00',
                team_number=20,
                country=dict(id=2, name='country2'),
                team=dict(id=2, name='team2')
            )
        ]
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/1/seasons/1/players")

    assert response.json() == expected_response
    mock_service_get_players.assert_called_once_with(1, 1)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint, service_args",
    [
        ("/leagues/1/seasons/999/players", (1, 999)),
        ("/leagues/999/seasons/1/players", (999, 1)),
    ]
)
@patch("api.leagues.service.get_players_in_season")
async def test_get_players_in_season_missing(mock_service_get_players, endpoint, service_args):
    mock_service_get_players.side_effect = Missing("Season not found")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(endpoint)

    assert response.status_code == 404
    assert response.json() == {"detail": "Season not found"}
    mock_service_get_players.assert_called_once_with(*service_args)


@pytest.mark.asyncio
@patch("api.leagues.service.get_scores_in_season")
async def test_get_scores_in_season(mock_service_get_scores):
    service_get_scores_return_value = SeasonWithTopPlayersSchema(
            id=1,
            name='2024/2025',
            players=[
                PlayerStatsSummarySchema(
                    id=1,
                    name='player1',
                    team_number=10,
                    team=BaseTeamSchema(id=1, name='team1'),
                    games=10,
                    effective_actions=15
                ),
                PlayerStatsSummarySchema(
                    id=2,
                    name='player2',
                    team_number=None,
                    team=BaseTeamSchema(id=2, name='team2'),
                    games=10,
                    effective_actions=0
                )
            ]
    )
    mock_service_get_scores.return_value = service_get_scores_return_value

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/1/seasons/1/scores")

    assert response.json() == service_get_scores_return_value.model_dump()
    mock_service_get_scores.assert_called_once_with(1, 1)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint, service_args",
    [
        ("/leagues/1/seasons/999/scores", (1, 999)),
        ("/leagues/999/seasons/1/scores", (999, 1)),
    ]
)
@patch("api.leagues.service.get_scores_in_season")
async def test_get_scores_in_season_missing(mock_service_get_scores, endpoint, service_args):
    mock_service_get_scores.side_effect = Missing("Season not found")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(endpoint)

    assert response.status_code == 404
    assert response.json() == {"detail": "Season not found"}
    mock_service_get_scores.assert_called_once_with(*service_args)
