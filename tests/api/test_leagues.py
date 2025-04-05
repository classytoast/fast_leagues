from unittest.mock import patch

import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from models.pydantic.leagues import LeagueSchema, SeasonSchema


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "service_return",
    [
        [
            LeagueSchema(
                id=1,
                name='APL',
                current_season=SeasonSchema(id=1, name='2024/2025',leader_id=23, leader_name='team1')
            ),
            LeagueSchema(
                id=2,
                name='Bundesliga',
                current_season=SeasonSchema(id=2, name='2024/2025', leader_id=15, leader_name='team2')
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
    service_get_one_return_value = LeagueSchema(
        id=1,
        name='APL',
        current_season=SeasonSchema(id=1, name='2024/2025', leader_id=23, leader_name='team1')
    )
    mock_service_get_one.return_value = service_get_one_return_value

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/1")

    assert response.json() == service_get_one_return_value.model_dump()
    mock_service_get_one.assert_called_once_with(1)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "service_return",
    [
        [
            SeasonSchema(
                id=1,
                name='2024/2025',
                league=LeagueSchema(id=1, name='APL'),
                leader_id=23,
                leader_name='team1'
            ),
            SeasonSchema(
                id=2,
                name='2024/2025',
                league=LeagueSchema(id=1, name='APL'),
                leader_id=10,
                leader_name='team2'
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
@patch("api.leagues.service.get_season")
async def test_get_season(mock_service_get_season):
    service_get_season_return_value = SeasonSchema(
            id=1,
            name='2024/2025',
            league=LeagueSchema(id=1, name='APL'),
            leader_id=23,
            leader_name='team1'
    )
    mock_service_get_season.return_value = service_get_season_return_value

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/leagues/1/seasons/1")

    assert response.json() == service_get_season_return_value.model_dump()
    mock_service_get_season.assert_called_once_with(1, 1)
