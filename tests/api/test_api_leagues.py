from unittest.mock import patch

import pytest
from httpx import AsyncClient, ASGITransport

from errors import Missing
from main import app
from models.pydantic.leagues import (
    CountrySchema,
    LeagueWithCurrentSeasonSchema,
    SeasonWithLeaderSchema, LeagueCountrySchema, SeasonRelSchema
)
from models.pydantic.teams import TeamSchema, TeamInSeasonSchema


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
                    teams=TeamSchema(
                        id=1,
                        name='team1',
                        founded='1900',
                        manager='manager1'
                    ))
            ),
            LeagueWithCurrentSeasonSchema(
                id=2,
                name='Bundesliga',
                country=CountrySchema(id=2, name='country2'),
                seasons=SeasonWithLeaderSchema(
                    id=2,
                    name='2024/2025',
                    teams=TeamSchema(
                        id=15,
                        name='team2',
                        founded='1905',
                        manager='manager2'
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
                teams=TeamSchema(
                    id=1,
                    name='team1',
                    founded='1900',
                    manager='manager1'
                )
            ),
            SeasonWithLeaderSchema(
                id=2,
                name='2024/2025',
                teams=TeamSchema(
                    id=2,
                    name='team2',
                    founded='1900',
                    manager='manager2'
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
