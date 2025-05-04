from datetime import datetime
from typing import Annotated, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.db.base import Base


if TYPE_CHECKING:
    from models.db.leagues import Country
    from models.db.teams import Team

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Person(Base):
    __tablename__ = "persons"
    id: Mapped[int_pk]
    name: Mapped[str]
    full_name: Mapped[str]
    birth_date: Mapped[datetime]
    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id", ondelete="SET NULL"),
        nullable=True
    )

    country: Mapped["Country"] = relationship(back_populates="persons")
    player: Mapped["Player"] = relationship(back_populates="person")
    manager: Mapped["Manager"] = relationship(back_populates="person")


class Player(Base):
    __tablename__ = "players"
    id: Mapped[int_pk]
    team_number: Mapped[int] = mapped_column(nullable=True, default=None)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        unique=True
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True
    )

    person: Mapped["Person"] = relationship(back_populates="player")
    team: Mapped["Team"] = relationship(back_populates="players")


class Manager(Base):
    __tablename__ = "managers"
    id: Mapped[int_pk]
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        unique=True
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),
        unique=True,
        nullable=True
    )

    person: Mapped["Person"] = relationship(back_populates="manager")
    team: Mapped["Team"] = relationship(back_populates="manager")
