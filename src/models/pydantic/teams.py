from typing import TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from models.pydantic.leagues import SeasonSchema, CountrySchema


class TeamSchema(BaseModel):
    id: int
    name: str
    founded: str
    manager: str
    country: "CountrySchema"
    current_seasons: list['SeasonSchema']
