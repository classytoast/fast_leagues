from typing import Annotated, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.db.base import Base


if TYPE_CHECKING:
    from models.db.teams import Team
    from models.db.persons import Person
    from models.db.games import Game


int_pk = Annotated[int, mapped_column(primary_key=True)]


class Country(Base):
    __tablename__ = "countries"
    id: Mapped[int_pk]
    name: Mapped[str]

    leagues: Mapped[list["League"]] = relationship(back_populates="country")
    teams: Mapped[list["Team"]] = relationship(back_populates="country")
    persons: Mapped[list["Person"]] = relationship(back_populates="country")


class League(Base):
    __tablename__ = "leagues"
    id: Mapped[int_pk]
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"))

    country: Mapped["Country"] = relationship(back_populates="leagues")
    seasons: Mapped[list["Season"]] = relationship(back_populates="league")


class Season(Base):
    __tablename__ = "seasons"
    id: Mapped[int_pk]
    name: Mapped[str]
    is_current_season: Mapped[bool] = mapped_column(default=False)
    league_id: Mapped[int] = mapped_column(ForeignKey("leagues.id", ondelete="CASCADE"))

    league: Mapped["League"] = relationship(back_populates="seasons")
    teams: Mapped[list["Team"]] = relationship(
        back_populates="seasons",
        secondary="seasons_teams"
    )
    games: Mapped[list["Game"]] = relationship(back_populates="season")
