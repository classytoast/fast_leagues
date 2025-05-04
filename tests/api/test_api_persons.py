from datetime import datetime
from unittest.mock import patch

import pytest
from httpx import AsyncClient, ASGITransport

from errors import Missing
from main import app
from models.pydantic.leagues import CountrySchema
from models.pydantic.persons import PlayerDetailsSchema, PersonDetailsSchema
from models.pydantic.teams import BaseTeamSchema


@pytest.mark.asyncio
@patch("api.persons.service.get_player")
async def test_get_player(mock_service_get_player):
    service_get_player_return_value = PlayerDetailsSchema(
        id=1,
        name='player1',
        full_name='full_player1',
        birth_date=datetime(2000, 1, 1),
        team_number=10,
        country=CountrySchema(id=1, name='country1'),
        team=BaseTeamSchema(id=1, name='team1')
    )
    mock_service_get_player.return_value = service_get_player_return_value

    expected_response = dict(
        id=1,
        name='player1',
        full_name='full_player1',
        birth_date='2000-01-01T00:00:00',
        team_number=10,
        country=dict(id=1, name='country1'),
        team=dict(id=1, name='team1')
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/players/1")

    assert response.json() == expected_response
    mock_service_get_player.assert_called_once()


@pytest.mark.asyncio
@patch("api.persons.service.get_player")
async def test_get_player_missing(mock_service_get_player):
    mock_service_get_player.side_effect = Missing("Player not found")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/players/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Player not found"}
    mock_service_get_player.assert_called_once_with(999)


@pytest.mark.asyncio
@patch("api.persons.service.get_manager")
async def test_get_manager(mock_service_get_manager):
    service_get_manager_return_value = PersonDetailsSchema(
        id=1,
        name='player1',
        full_name='full_player1',
        birth_date=datetime(2000, 1, 1),
        country=CountrySchema(id=1, name='country1'),
        team=BaseTeamSchema(id=1, name='team1')
    )
    mock_service_get_manager.return_value = service_get_manager_return_value

    expected_response = dict(
        id=1,
        name='player1',
        full_name='full_player1',
        birth_date='2000-01-01T00:00:00',
        country=dict(id=1, name='country1'),
        team=dict(id=1, name='team1')
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/managers/1")

    assert response.json() == expected_response
    mock_service_get_manager.assert_called_once()


@pytest.mark.asyncio
@patch("api.persons.service.get_manager")
async def test_get_manager_missing(mock_service_get_manager):
    mock_service_get_manager.side_effect = Missing("Player not found")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/managers/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Player not found"}
    mock_service_get_manager.assert_called_once_with(999)
