from sqlmodel import Field, SQLModel

class GameBase(SQLModel):
    week: int
    home_team: str
    away_team: str
    home_score: int | None = None
    away_score: int | None = None

class Game(GameBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ReadGame(GameBase):
    id: int

class CreateGame(GameBase):
    pass


# TODO: 
# Add constraints (week #'s)
# Make types strict i.e. can't add extra fields to a create
# UUIDs