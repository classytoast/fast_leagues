from datetime import datetime
from unittest.mock import patch, Mock

import pytest

from services.games import (
    get_game,
    get_games_for_date
)


@pytest.mark.asyncio
@patch("services.games.data.get_game")
async def test_get_game(mock_repo_get_game):
    repo_return = Mock()
    mock_repo_get_game.return_value = repo_return

    result = await get_game(1)

    assert result == repo_return
    mock_repo_get_game.assert_called_once()


@pytest.mark.asyncio
@patch("services.games.data.get_games_for_date")
async def test_get_games_for_date(mock_repo_get_games):
    repo_return = [Mock(), Mock()]
    mock_repo_get_games.return_value = repo_return

    result = await get_games_for_date(datetime(2025, 1, 1))

    assert result == repo_return
    mock_repo_get_games.assert_called_once_with(datetime(2025, 1, 1))
