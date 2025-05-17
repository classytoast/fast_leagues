from datetime import datetime
from unittest.mock import patch
from contextlib import nullcontext as not_raise

import pytest

from errors import Missing
from repositories.teams import (
    get_all_teams,
    get_one_team,
    get_games_for_team
)


@pytest.mark.asyncio
@patch("repositories.teams.async_session")
async def test_get_all_teams(mock_session, db_session, leagues_data):
    mock_session.return_value = db_session

    result = await get_all_teams()

    assert len(result) == 3

    assert (result[0].id, result[0].name, result[0].founded) == (1, 'team1', "1900")
    assert (result[0].manager.id, result[0].manager.name) == (1, 'person5')

    assert (result[1].id, result[1].name, result[1].founded) == (2, 'team2', "1901")
    assert (result[1].manager.id, result[1].manager.name) == (2, 'person6')

    assert (result[2].id, result[2].name, result[2].founded) == (3, 'team3', "1902")
    assert result[2].manager is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "team_id, expected_team, expected_manager, expected_country, expected_seasons, expected_players, expectation",
    [
        (1, (1, 'team1'), (1, 'person5'), (1, 'country1'), [(1, 'season1'), (3, 'season3')],
         [(1, 'person1', 10), (2, 'person2', 11)], not_raise()),

        (3, (3, 'team3'), None, (2, 'country2'), [(3, 'season3')],
         [(4, 'person4', 13)], not_raise()),

        (6, None, None, None, None, None, pytest.raises(Missing)),
    ]
)
@patch("repositories.teams.async_session")
async def test_get_one_team(mock_session, db_session, team_id, expected_team, expected_manager, expected_country,
                            expected_seasons, expected_players, expectation, leagues_data):
    mock_session.return_value = db_session

    with expectation:
        result = await get_one_team(team_id)

        assert (result.id, result.name) == expected_team
        if expected_manager is not None:
            assert (result.manager.id, result.manager.name) == expected_manager
        else:
            assert result.manager is None
        assert (result.country.id, result.country.name) == expected_country
        seasons = result.current_seasons
        assert len(seasons) == len(expected_seasons)
        assert [(s.id, s.name) for s in seasons] == expected_seasons
        players = result.players
        assert len(players) == len(expected_players)
        assert [(p.id, p.name, p.team_number) for p in players] == expected_players


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "team_id, expected_result, expectation",
    [
        (1,
         dict(
             id=1,
             name='team1',
             games=[
                 dict(id=2, game_date=datetime(2025, 2, 1),
                      home_team=dict(id=3, name='team3'), guest_team=dict(id=1, name='team1'),
                      home_scored=2, guest_scored=2),
                 dict(id=1, game_date=datetime(2025, 1, 1),
                      home_team=dict(id=1, name='team1'), guest_team=dict(id=2, name='team2'),
                      home_scored=2, guest_scored=1),
             ]
         ),
         not_raise()),

        (3,
         dict(
             id=3,
             name='team3',
             games=[
                 dict(id=2, game_date=datetime(2025, 2, 1),
                      home_team=dict(id=3, name='team3'), guest_team=dict(id=1, name='team1'),
                      home_scored=2, guest_scored=2),
             ]
         ),
         not_raise()),

        (999, None, pytest.raises(Missing)),
    ]
)
@patch("repositories.teams.async_session")
async def test_get_games_for_team(mock_session, team_id, expected_result,
                                  expectation, db_session, leagues_data):
    mock_session.return_value = db_session

    with expectation:
        result = await get_games_for_team(team_id)

        assert result.id == expected_result['id']
        assert result.name == expected_result['name']

        for idx in range(len(result.games)):
            assert result.games[idx].id == expected_result['games'][idx]['id']
            assert result.games[idx].game_date == expected_result['games'][idx]['game_date']
            assert dict(result.games[idx].home_team) == expected_result['games'][idx]['home_team']
            assert dict(result.games[idx].guest_team) == expected_result['games'][idx]['guest_team']
            assert result.games[idx].home_scored == expected_result['games'][idx]['home_scored']
            assert result.games[idx].guest_scored == expected_result['games'][idx]['guest_scored']

