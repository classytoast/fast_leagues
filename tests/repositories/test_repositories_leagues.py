from unittest.mock import patch

import pytest

from repositories.leagues import get_all_leagues


@pytest.mark.asyncio
@patch("repositories.leagues.async_session")
async def test_get_all_leagues(mock_session, db_session, leagues_data):
    mock_session.return_value = db_session

    result = await get_all_leagues()

    assert (result[0].id, result[0].name) == (1, 'league1')
    assert (result[0].country.id, result[0].country.name) == (1, 'country1')
    season = result[0].current_season
    assert (season.id, season.name, season.leader_id, season.leader_name) == (2, 'season2', 0, 'mock_team')

    assert (result[1].id, result[1].name) == (2, 'league2')
    assert (result[1].country.id, result[1].country.name) == (1, 'country1')
    season = result[1].current_season
    assert (season.id, season.name, season.leader_id, season.leader_name) == (4, 'season4', 0, 'mock_team')

    assert (result[2].id, result[2].name) == (3, 'league3')
    assert (result[2].country.id, result[2].country.name) == (2, 'country2')
    season = result[2].current_season
    assert (season.id, season.name, season.leader_id, season.leader_name) == (5, 'season5', 0, 'mock_team')
