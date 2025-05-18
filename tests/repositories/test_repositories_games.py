from contextlib import nullcontext as not_raise
from datetime import datetime
from unittest.mock import patch

import pytest

from errors import Missing
from repositories.games import (
    get_game,
    get_games_for_date
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "game_id, expected_game, expectation",
    [
        (1,
         dict(
             id=1,
             season=dict(id=1, name='season1'),
             game_date=datetime(2025, 1, 1),
             home_team=dict(id=1, name='team1'),
             guest_team=dict(id=2, name='team2'),
             home_scored=2,
             guest_scored=1,
             home_team_composition=[dict(id=1, name='person1', status='starting lineups', team_number=None),
                                    dict(id=2, name='person2', status='starting lineups', team_number=None)],
             guest_team_composition=[dict(id=3, name='person3', status='starting lineups', team_number=None)],
             home_manager=dict(id=1, name='person5'),
             guest_manager=dict(id=2, name='person6'),
             game_events=[dict(event_type='goal', minute='23'),
                          dict(event_type='goal', minute='30'),
                          dict(event_type='assist', minute='30'),
                          dict(event_type='goal', minute='68'),
                          dict(event_type='goal', minute='90'),
                          dict(event_type='yellow_card', minute='45'),
                          dict(event_type='red_card', minute='70'),
                          dict(event_type='unrealized_penalty_goal', minute='35'),]
         ),
         not_raise()),

        (2,
         dict(
             id=2,
             season=dict(id=3, name='season3'),
             game_date=datetime(2025, 2, 1),
             home_team=dict(id=3, name='team3'),
             guest_team=dict(id=1, name='team1'),
             home_scored=2,
             guest_scored=2,
             home_team_composition=[dict(id=4, name='person4', status='starting lineups', team_number=None)],
             guest_team_composition=[dict(id=1, name='person1', status='starting lineups', team_number=None),
                                     dict(id=2, name='person2', status='substitutes', team_number=None)],
             home_manager=None,
             guest_manager=dict(id=1, name='person5'),
             game_events=[]
         ),
         not_raise()),

        (10, None, pytest.raises(Missing)),
    ]
)
@patch("repositories.games.async_session")
async def test_get_game(mock_session, game_id, expected_game, expectation, db_session, leagues_data):
    mock_session.return_value = db_session

    with expectation:
        result = await get_game(game_id)

        assert result.id == expected_game["id"]
        assert dict(result.season) == expected_game["season"]
        assert result.game_date == expected_game["game_date"]
        assert dict(result.home_team) == expected_game["home_team"]
        assert dict(result.guest_team) == expected_game["guest_team"]
        assert result.home_scored == expected_game["home_scored"]
        assert result.guest_scored == expected_game["guest_scored"]
        assert [dict(x) for x in result.home_team_composition] == expected_game["home_team_composition"]
        assert [dict(x) for x in result.guest_team_composition] == expected_game["guest_team_composition"]

        if expected_game['home_manager'] is not None:
            assert dict(result.home_manager) == expected_game["home_manager"]
        else:
            assert result.home_manager is None

        if expected_game['guest_manager'] is not None:
            assert dict(result.guest_manager) == expected_game["guest_manager"]
        else:
            assert result.guest_manager is None

        assert [(x.event_type, x.minute) for x in result.game_events] == [
            (x['event_type'], x['minute']) for x in expected_game["game_events"]]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date, expected_games",
    [
        (datetime(2025, 1, 1),
         [
             dict(
                 id=1,
                 season=dict(id=1, name='season1'),
                 league=dict(id=1, name='league1'),
                 game_date=datetime(2025, 1, 1),
                 home_team=dict(id=1, name='team1'),
                 guest_team=dict(id=2, name='team2'),
                 home_scored=2,
                 guest_scored=1,
             )
         ]),

        (datetime(2020, 1, 1), []),
    ]
)
@patch("repositories.games.async_session")
async def test_get_games_for_date(mock_session, date, expected_games, db_session, leagues_data):
    mock_session.return_value = db_session

    result = await get_games_for_date(date)

    for idx in range(len(result)):
        assert result[idx].id == expected_games[idx]['id']
        assert dict(result[idx].season) == dict(expected_games[idx]['season'])
        assert dict(result[idx].league) == dict(expected_games[idx]['league'])
        assert result[idx].game_date == expected_games[idx]['game_date']
        assert dict(result[idx].home_team) == dict(expected_games[idx]['home_team'])
        assert dict(result[idx].guest_team) == dict(expected_games[idx]['guest_team'])
        assert result[idx].home_scored == expected_games[idx]['home_scored']
        assert result[idx].guest_scored == expected_games[idx]['guest_scored']
