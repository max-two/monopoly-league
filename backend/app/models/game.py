from sqlmodel import Field, SQLModel

class GameBase(SQLModel):
    week: int = Field(ge=1, le=22)
    home_team: str
    away_team: str
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)

class Game(GameBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ReadGame(GameBase):
    id: int

class CreateGame(GameBase):
    pass


# TODO: 
# Make teams enums
# Make types strict i.e. can't add extra fields to a create
# UUIDs