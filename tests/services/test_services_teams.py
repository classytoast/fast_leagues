from unittest.mock import patch, Mock

import pytest

from services.teams import get_all_teams, get_one_team


@pytest.mark.asyncio
@patch("services.teams.data.get_all_teams")
async def test_get_all_leagues(mock_repo_get_all):
    repo_return = [Mock(), Mock()]
    mock_repo_get_all.return_value = repo_return

    result = await get_all_teams()

    assert result == repo_return
    mock_repo_get_all.assert_called_once()


@pytest.mark.asyncio
@patch("services.teams.data.get_one_team")
async def test_get_one_league(mock_repo_get_one):
    repo_return = Mock()
    mock_repo_get_one.return_value = repo_return

    result = await get_one_team(1)

    assert result == repo_return
    mock_repo_get_one.assert_called_once_with(1)
