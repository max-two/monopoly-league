from sqlmodel import Field, SQLModel


class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    week: int = Field(index=True)
    home_team: str = Field(index=True)
    away_team: str = Field(index=True)
    home_score: int | None = Field(default=None)
    away_score: int | None = Field(default=None)

# TODO:nullable id? make scores unsigned? why is the list return nullable?