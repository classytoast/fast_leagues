from datetime import datetime
from unittest.mock import patch
from contextlib import nullcontext as not_raise

import pytest

from errors import Missing
from repositories.persons import get_player, get_manager


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "player_id, expected_player, expected_country, expected_team, expectation",
    [
        (1, (1, 'person1', "complete1", datetime(2000, 1, 1), 10),
         (1, 'country1'), (1, 'team1'), not_raise()),

        (3, (3, 'person3', "complete3", datetime(2000, 3, 1), 12),
         (2, 'country2'), (2, 'team2'), not_raise()),

        (5, (5, 'person8', "complete8", datetime(1990, 1, 1), None),
         (1, 'country1'), None, not_raise()),

        (10, None, None, None, pytest.raises(Missing)),
    ]
)
@patch("repositories.persons.async_session")
async def test_get_player(mock_session, db_session, player_id, expected_player, expected_country,
                          expected_team, expectation, leagues_data):
    mock_session.return_value = db_session

    with expectation:
        result = await get_player(player_id)

        assert (result.id, result.name, result.full_name, result.birth_date, result.team_number) == expected_player
        country = result.country
        assert (country.id, country.name) == expected_country
        team = result.team
        if expected_team is not None:
            assert (team.id, team.name) == expected_team
        else:
            assert team is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "manager_id, expected_manager, expected_country, expected_team, expectation",
    [
        (1, (1, 'person5', "complete5", datetime(1980, 1, 1)),
         (1, 'country1'), (1, 'team1'), not_raise()),

        (3, (3, 'person7', "complete7", datetime(1980, 3, 1)),
         (2, 'country2'), None, not_raise()),

        (10, None, None, None, pytest.raises(Missing)),
    ]
)
@patch("repositories.persons.async_session")
async def test_get_manager(mock_session, db_session, manager_id, expected_manager, expected_country,
                           expected_team, expectation, leagues_data):
    mock_session.return_value = db_session

    with expectation:
        result = await get_manager(manager_id)

        assert (result.id, result.name, result.full_name, result.birth_date) == expected_manager
        country = result.country
        assert (country.id, country.name) == expected_country
        team = result.team
        if expected_team is not None:
            assert (team.id, team.name) == expected_team
        else:
            assert team is None
