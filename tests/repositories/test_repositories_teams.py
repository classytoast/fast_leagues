from unittest.mock import patch
from contextlib import nullcontext as not_raise

import pytest

from errors import Missing
from repositories.teams import get_all_teams, get_one_team


@pytest.mark.asyncio
@patch("repositories.teams.async_session")
async def test_get_all_teams(mock_session, db_session, leagues_data):
    mock_session.return_value = db_session

    result = await get_all_teams()

    assert len(result) == 3

    assert (result[0].id, result[0].name) == (1, 'team1')
    assert (result[0].country.id, result[0].country.name) == (1, 'country1')
    seasons = result[0].current_seasons
    assert len(seasons) == 2
    assert (seasons[0].id, seasons[0].name) == (1, 'season1')
    assert (seasons[1].id, seasons[1].name) == (3, 'season3')

    assert (result[1].id, result[1].name) == (2, 'team2')
    assert (result[1].country.id, result[1].country.name) == (1, 'country1')
    seasons = result[1].current_seasons
    assert len(seasons) == 1
    assert (seasons[0].id, seasons[0].name) == (1, 'season1')

    assert (result[2].id, result[2].name) == (3, 'team3')
    assert (result[2].country.id, result[2].country.name) == (2, 'country2')
    seasons = result[2].current_seasons
    assert len(seasons) == 1
    assert (seasons[0].id, seasons[0].name) == (3, 'season3')


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "team_id, expected_team, expected_country, expected_seasons, expectation",
    [
        (1, (1, 'team1'), (1, 'country1'), [(1, 'season1'), (3, 'season3')], not_raise()),

        (3, (3, 'team3'), (2, 'country2'), [(3, 'season3')], not_raise()),

        (6, None, None, None, pytest.raises(Missing)),
    ]
)
@patch("repositories.teams.async_session")
async def test_get_one_team(mock_session, db_session, team_id, expected_team, expected_country,
                            expected_seasons, expectation, leagues_data):
    mock_session.return_value = db_session

    with expectation:
        result = await get_one_team(team_id)

        assert (result.id, result.name) == expected_team
        assert (result.country.id, result.country.name) == expected_country
        seasons = result.current_seasons
        assert len(seasons) == len(expected_seasons)
        assert [(s.id, s.name) for s in seasons] == expected_seasons

