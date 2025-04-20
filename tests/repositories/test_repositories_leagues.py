from unittest.mock import patch
from contextlib import nullcontext as not_raise

import pytest

from errors import Missing
from repositories.leagues import get_all_leagues, get_one_league, get_seasons


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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "league_id, expected_result, expectation",
    [
        (1, (1, 'league1', 1, 'country1'), not_raise()),

        (3, (3, 'league3', 2, 'country2'), not_raise()),

        (6, None, pytest.raises(Missing)),
    ]
)
@patch("repositories.leagues.async_session")
async def test_get_one_league(mock_session, league_id, expected_result, expectation, db_session, leagues_data):
    mock_session.return_value = db_session

    with expectation:
        result = await get_one_league(league_id)

        assert result.id == expected_result[0]
        assert result.name == expected_result[1]
        assert result.country.id == expected_result[2]
        assert result.country.name == expected_result[3]
        assert result.current_season is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "league_id, expectation",
    [
        (1, not_raise()),

        (6, pytest.raises(Missing)),
    ]
)
@patch("repositories.leagues.async_session")
async def test_get_seasons(mock_session, league_id, expectation, db_session, leagues_data):
    mock_session.return_value = db_session

    with expectation:
        result = await get_seasons(league_id)

        season = result[0]
        assert (season.id, season.name, season.leader_id, season.leader_name) == (1, 'season1', 0, 'mock_team')
        season = result[1]
        assert (season.id, season.name, season.leader_id, season.leader_name) == (2, 'season2', 0, 'mock_team')
