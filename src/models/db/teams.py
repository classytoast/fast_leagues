from typing import Annotated, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.db.base import Base


if TYPE_CHECKING:
    from models.db.leagues import Country, Season

int_pk = Annotated[int, mapped_column(primary_key=True)]
int_default_0 = Annotated[int, mapped_column(default=0)]


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int_pk]
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"))
    founded: Mapped[str]
    manager: Mapped[str]

    country: Mapped["Country"] = relationship(back_populates="teams")
    seasons: Mapped[list["Season"]] = relationship(
        back_populates="teams",
        secondary="seasons_teams"
    )


class SeasonTeam(Base):
    __tablename__ = "seasons_teams"
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id", ondelete="CASCADE"),
        primary_key=True
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"),
        primary_key=True
    )

    position: Mapped[int_default_0]
    games: Mapped[int_default_0]
    wins: Mapped[int_default_0]
    draws: Mapped[int_default_0]
    loses: Mapped[int_default_0]
    scored_goals: Mapped[int_default_0]
    conceded_goals: Mapped[int_default_0]
    points: Mapped[int_default_0]
