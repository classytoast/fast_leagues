from datetime import datetime

import pytest_asyncio
from sqlalchemy import delete

from database import init_mongo_db
from models.db.games import Game
from models.db.leagues import League, Country, Season
from models.db.persons import Person, Player, Manager
from models.db.teams import Team, SeasonTeam
from models.mongo_documents.games import (
    PersonEmbeddedObject,
    EventEmbeddedObject,
    EventType,
    GameDocument, TeamEmbeddedObject
)


@pytest_asyncio.fixture(scope="function")
async def db_session(session_factory, setup_database):
    session = session_factory()
    yield session
    await session.rollback()
    await session.close()


@pytest_asyncio.fixture(scope="function")
async def leagues_data(db_session, games_mongo_data):
    await db_session.execute(delete(League))
    await db_session.execute(delete(Country))
    await db_session.execute(delete(Season))
    await db_session.execute(delete(Team))
    await db_session.execute(delete(SeasonTeam))
    await db_session.execute(delete(Person))
    await db_session.execute(delete(Player))
    await db_session.execute(delete(Manager))
    await db_session.execute(delete(Game))

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
        Team(id=1, name='team1', country_id=1, founded="1900"),
        Team(id=2, name='team2', country_id=1, founded="1901"),
        Team(id=3, name='team3', country_id=2, founded="1902")
    ]

    db_session.add_all([
        Person(id=1, name='person1', full_name="complete1",
               birth_date=datetime(2000, 1, 1), country_id=1),
        Person(id=2, name='person2', full_name="complete2",
               birth_date=datetime(2000, 2, 1), country_id=1),
        Person(id=3, name='person3', full_name="complete3",
               birth_date=datetime(2000, 3, 1), country_id=2),
        Person(id=4, name='person4', full_name="complete4",
               birth_date=datetime(2000, 4, 1), country_id=2),
        Person(id=5, name='person5', full_name="complete5",
               birth_date=datetime(1980, 1, 1), country_id=1),
        Person(id=6, name='person6', full_name="complete6",
               birth_date=datetime(1980, 2, 1), country_id=2),
        Person(id=7, name='person7', full_name="complete7",
               birth_date=datetime(1980, 3, 1), country_id=2),
        Person(id=8, name='person8', full_name="complete8",
               birth_date=datetime(1990, 1, 1), country_id=1),
    ])

    db_session.add_all([
        Player(id=1, team_number=10, person_id=1, team_id=1),
        Player(id=2, team_number=11, person_id=2, team_id=1),
        Player(id=3, team_number=12, person_id=3, team_id=2),
        Player(id=4, team_number=13, person_id=4, team_id=3),
        Player(id=5, team_number=None, person_id=8, team_id=None),
    ])

    db_session.add_all([
        Manager(id=1, person_id=5, team_id=1),
        Manager(id=2, person_id=6, team_id=2),
        Manager(id=3, person_id=7, team_id=None),
    ])

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

    db_session.add_all([
        Game(id=1, game_date=datetime(2025, 1, 1), season_id=1, home_team_id=1,
             guest_team_id=2, home_scored=2, guest_scored=1),
        Game(id=2, game_date=datetime(2025, 2, 1), season_id=3, home_team_id=3,
             guest_team_id=1, home_scored=2, guest_scored=2),
    ])

    await db_session.commit()


@pytest_asyncio.fixture(scope="function")
async def games_mongo_data():
    await init_mongo_db()

    team1 = TeamEmbeddedObject(id=1, name="team1")
    team2 = TeamEmbeddedObject(id=2, name="team2")
    team3 = TeamEmbeddedObject(id=3, name="team3")

    player1 = PersonEmbeddedObject(id=1, name="person1", team=team1)
    player2 = PersonEmbeddedObject(id=2, name="person2", team=team1)
    player3 = PersonEmbeddedObject(id=3, name="person3", team=team2)
    player4 = PersonEmbeddedObject(id=4, name="person4", team=team3)
    manager1 = PersonEmbeddedObject(id=1, name="person5", team=team1)
    manager2 = PersonEmbeddedObject(id=2, name="person6", team=team2)

    game1 = GameDocument(
        game_id=1,
        season_id=1,
        league_id=1,
        home_start_composition=[player1, player2],
        guest_start_composition=[player3],
        home_manager=manager1,
        guest_manager=manager2,
        events=[
            EventEmbeddedObject(event_type=EventType.goal, minute="23", person=player1),
            EventEmbeddedObject(event_type=EventType.goal, minute="30", person=player2),
            EventEmbeddedObject(event_type=EventType.assist, minute="30", person=player1),
            EventEmbeddedObject(event_type=EventType.goal, minute="68", person=player3),
            EventEmbeddedObject(event_type=EventType.goal, minute="90", person=player3),
            EventEmbeddedObject(event_type=EventType.yellow_card, minute="45", person=player1),
            EventEmbeddedObject(event_type=EventType.red_card, minute="70", person=player1),
            EventEmbeddedObject(event_type=EventType.unrealized_penalty_goal, minute="35", person=player3),
        ]
    )

    game2 = GameDocument(
        game_id=2,
        season_id=3,
        league_id=2,
        home_start_composition=[player4],
        guest_start_composition=[player1],
        guest_substitution=[player2],
        guest_manager=manager1,
    )

    await game1.insert()
    await game2.insert()

    yield

    # Очистка после теста
    await GameDocument.find({"game_id": game1.game_id}).delete()
    await GameDocument.find({"game_id": game2.game_id}).delete()
