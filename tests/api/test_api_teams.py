from unittest.mock import patch

import pytest
from httpx import AsyncClient, ASGITransport

from errors import Missing
from main import app
from models.pydantic.leagues import (
    CountrySchema,
    SeasonSchema
)
from models.pydantic.persons import BasePersonSchema, BasePlayerSchema
from models.pydantic.teams import TeamRelSchema, TeamDetailsSchema


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "service_return",
    [
        [
            TeamDetailsSchema(
                id=1,
                name='team1',
                founded='1900',
                manager=BasePersonSchema(id=1, name='person1')
            ),
            TeamDetailsSchema(
                id=2,
                name='team2',
                founded='1905',
                manager=None
            ),
        ],
        []
    ]
)
@patch("api.teams.service.get_all_teams")
async def test_get_all_teams(mock_service_get_all, service_return):
    mock_service_get_all.return_value = service_return

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/teams/")

    assert response.json() == [m.model_dump() for m in service_return]
    mock_service_get_all.assert_called_once()


@pytest.mark.asyncio
@patch("api.teams.service.get_one_team")
async def test_get_one_team(mock_service_get_one):
    service_get_one_return_value = TeamRelSchema(
        id=1,
        name='team1',
        founded='1900',
        manager=BasePersonSchema(id=1, name='person1'),
        country=CountrySchema(id=1, name='country1'),
        seasons=[
            SeasonSchema(id=1, name='2024/2025')
        ],
        players=[
            BasePlayerSchema(id=1, name='person2', team_number=10),
            BasePlayerSchema(id=2, name='person3', team_number=11),
        ]
    )
    mock_service_get_one.return_value = service_get_one_return_value

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/teams/1")

    assert response.json() == service_get_one_return_value.model_dump()
    mock_service_get_one.assert_called_once_with(1)


@pytest.mark.asyncio
@patch("api.teams.service.get_one_team")
async def test_get_one_team_missing(mock_service_get_one):
    mock_service_get_one.side_effect = Missing("Team not found")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/teams/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Team not found"}
    mock_service_get_one.assert_called_once_with(999)
