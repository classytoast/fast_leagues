import pytest_asyncio
from sqlalchemy import delete

from models.db.leagues import League, Country, Season
from models.db.teams import Team, SeasonTeam


@pytest_asyncio.fixture(scope="function")
async def db_session(session_factory, setup_database):
    session = session_factory()
    yield session
    await session.rollback()
    await session.close()


@pytest_asyncio.fixture(scope="function")
async def leagues_data(db_session):
    await db_session.execute(delete(League))
    await db_session.execute(delete(Country))
    await db_session.execute(delete(Season))
    await db_session.execute(delete(Team))
    await db_session.execute(delete(SeasonTeam))

    db_session.add_all([
        Country(id=1, name='country1'),
        Country(id=2, name='country2')
    ])

    db_session.add_all([
        League(id=1, name='league1', country_id=1),
        League(id=2, name='league2', country_id=1),
        League(id=3, name='league3', country_id=2)
    ])

    seasons = [
        Season(id=1, name='season1', league_id=1, is_current_season=True),
        Season(id=2, name='season2', league_id=1, is_current_season=False),
        Season(id=3, name='season3', league_id=2, is_current_season=True),
        Season(id=4, name='season4', league_id=2, is_current_season=False),
        Season(id=5, name='season5', league_id=3, is_current_season=True),
    ]

    teams = [
        Team(id=1, name='team1', country_id=1, manager='manager', founded="1900"),
        Team(id=2, name='team2', country_id=1, manager='manager', founded="1900"),
        Team(id=3, name='team3', country_id=2, manager='manager', founded="1900")
    ]

    stats_data = [
        # season_id, team_id, position, games, wins, draws, loses, scored, conceded, points
        (1, 1, 1, 1, 1, 0, 0, 2, 1, 3),
        (1, 2, 2, 1, 0, 0, 1, 1, 2, 0),
        (3, 1, 5, 1, 0, 1, 0, 2, 2, 1),
        (3, 3, 1, 1, 0, 1, 0, 2, 2, 1),
    ]
    for data in stats_data:
        db_session.add(SeasonTeam(
            season_id=data[0],
            team_id=data[1],
            position=data[2],
            games=data[3],
            wins=data[4],
            draws=data[5],
            loses=data[6],
            scored_goals=data[7],
            conceded_goals=data[8],
            points=data[9]
        ))

    db_session.add_all(seasons)
    db_session.add_all(teams)

    await db_session.commit()
