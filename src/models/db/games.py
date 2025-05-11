from datetime import datetime
from typing import Annotated, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.db.base import Base


if TYPE_CHECKING:
    from models.db.leagues import Season
    from models.db.teams import Team


int_pk = Annotated[int, mapped_column(primary_key=True)]


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int_pk]
    game_date: Mapped[datetime] = mapped_column(nullable=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete="CASCADE"))
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    guest_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    home_scored: Mapped[int] = mapped_column(nullable=True)
    guest_scored: Mapped[int] = mapped_column(nullable=True)

    season: Mapped["Season"] = relationship(back_populates="games")
    home_team: Mapped["Team"] = relationship(back_populates="home_games", foreign_keys=[home_team_id])
    guest_team: Mapped["Team"] = relationship(back_populates="guest_games", foreign_keys=[guest_team_id])
