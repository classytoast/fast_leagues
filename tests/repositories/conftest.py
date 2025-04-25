import pytest_asyncio
from sqlalchemy import delete

from models.db.leagues import League, Country, Season


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

    db_session.add_all([
        Country(id=1, name='country1'),
        Country(id=2, name='country2')
    ])

    db_session.add_all([
        League(id=1, name='league1', country_id=1),
        League(id=2, name='league2', country_id=1),
        League(id=3, name='league3', country_id=2)
    ])

    db_session.add_all([
        Season(id=1, name='season1', league_id=1),
        Season(id=2, name='season2', league_id=1),
        Season(id=3, name='season3', league_id=2),
        Season(id=4, name='season4', league_id=2),
        Season(id=5, name='season5', league_id=3),
    ])

    await db_session.commit()
