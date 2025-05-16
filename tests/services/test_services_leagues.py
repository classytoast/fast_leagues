from unittest.mock import patch, Mock

import pytest

from services.leagues import (
    get_all_leagues,
    get_one_league,
    get_seasons,
    get_season,
    get_players_in_season, get_scores_in_season
)


@pytest.mark.asyncio
@patch("services.leagues.data.get_all_leagues")
async def test_get_all_leagues(mock_repo_get_all):
    repo_return = [Mock(), Mock()]
    mock_repo_get_all.return_value = repo_return

    result = await get_all_leagues()

    assert result == repo_return
    mock_repo_get_all.assert_called_once()


@pytest.mark.asyncio
@patch("services.leagues.data.get_one_league")
async def test_get_one_league(mock_repo_get_one):
    repo_return = Mock()
    mock_repo_get_one.return_value = repo_return

    result = await get_one_league(1)

    assert result == repo_return
    mock_repo_get_one.assert_called_once_with(1)


@pytest.mark.asyncio
@patch("services.leagues.data.get_seasons")
async def test_get_seasons(mock_repo_get_seasons):
    repo_return = [Mock(), Mock()]
    mock_repo_get_seasons.return_value = repo_return

    result = await get_seasons(1)

    assert result == repo_return
    mock_repo_get_seasons.assert_called_once_with(1)


@pytest.mark.asyncio
@patch("services.leagues.data.get_season")
async def test_get_season(mock_repo_get_season):
    repo_return = Mock()
    mock_repo_get_season.return_value = repo_return

    result = await get_season(1, 2)

    assert result == repo_return
    mock_repo_get_season.assert_called_once_with(1, 2)


@pytest.mark.asyncio
@patch("services.leagues.data.get_players_in_season")
async def test_get_players_in_season(mock_repo_get_players):
    repo_return = Mock()
    mock_repo_get_players.return_value = repo_return

    result = await get_players_in_season(1, 2)

    assert result == repo_return
    mock_repo_get_players.assert_called_once_with(1, 2)


@pytest.mark.asyncio
@patch("services.leagues.data.get_scores_in_season")
async def test_get_scores_in_season(mock_repo_get_scores):
    repo_return = Mock()
    mock_repo_get_scores.return_value = repo_return

    result = await get_scores_in_season(1, 2)

    assert result == repo_return
    mock_repo_get_scores.assert_called_once_with(1, 2)
