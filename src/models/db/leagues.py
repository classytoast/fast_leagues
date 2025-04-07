from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.db.base import Base


int_pk = Annotated[int, mapped_column(primary_key=True)]


class Country(Base):
    __tablename__ = "countries"
    id: Mapped[int_pk]
    name: Mapped[str]

    leagues: Mapped[list["League"]] = relationship()


class League(Base):
    __tablename__ = "leagues"
    id: Mapped[int_pk]
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"))

    country: Mapped["Country"] = relationship(back_populates="leagues")
    seasons: Mapped[list["Season"]] = relationship()


class Season(Base):
    __tablename__ = "seasons"
    id: Mapped[int_pk]
    name: Mapped[str]
    league_id: Mapped[int] = mapped_column(ForeignKey("leagues.id", ondelete="CASCADE"))

    league: Mapped["League"] = relationship(back_populates="seasons")
