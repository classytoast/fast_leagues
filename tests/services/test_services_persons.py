from unittest.mock import patch, Mock

import pytest

from services.persons import get_manager, get_player


@pytest.mark.asyncio
@patch("services.persons.data.get_player")
async def test_get_player(mock_repo_get_player):
    repo_return = [Mock(), Mock()]
    mock_repo_get_player.return_value = repo_return

    result = await get_player(1)

    assert result == repo_return
    mock_repo_get_player.assert_called_once()


@pytest.mark.asyncio
@patch("services.persons.data.get_manager")
async def test_get_manager(mock_repo_get_manager):
    repo_return = Mock()
    mock_repo_get_manager.return_value = repo_return

    result = await get_manager(1)

    assert result == repo_return
    mock_repo_get_manager.assert_called_once_with(1)
