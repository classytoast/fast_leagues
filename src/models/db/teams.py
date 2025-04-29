from typing import Annotated, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.db.base import Base


if TYPE_CHECKING:
    from models.db.leagues import Country

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int_pk]
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"))
    founded: Mapped[str]
    manager: Mapped[str]

    country: Mapped["Country"] = relationship(back_populates="teams")
    seasons: Mapped[list["SeasonTeam"]] = relationship(
        back_populates="teams_in_season",
        secondary="season_teams"
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
