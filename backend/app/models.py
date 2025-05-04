from enum import Enum
from uuid import uuid4, UUID

from sqlmodel import Field, Relationship, SQLModel

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

def PkField():
    return Field(default_factory=uuid4, primary_key=True)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Game
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NflTeam(str, Enum):
    BEARS = "Bears"
    LIONS = "Lions"
    PACKERS = "Packers"
    VIKINGS = "Vikings"
    COWBOYS = "Cowboys"
    FALCONS = "Falcons"
    PANTHERS = "Panthers"
    SAINTS = "Saints"
    SEAHAWKS = "Seahawks"
    TITANS = "Titans"
    BRONCOS = "Broncos"
    JETS = "Jets"
    DOLPHINS = "Dolphins"
    BROWNS = "Browns"
    PATRIOTS = "Patriots"
    JAGUARS = "Jaguars"
    COLTS = "Colts"
    RAIDERS = "Raiders"
    CHIEFS = "Chiefs"
    CHARGERS = "Chargers"
    COMMANDERS = "Commanders"
    GIANTS = "Giants"
    EAGLES = "Eagles"
    CARDINALS = "Cardinals"
    RAMS = "Rams"
    FORTY_NINERS = "49ers"
    BILLS = "Bills"
    STEELERS = "Steelers"
    RAVENS = "Ravens"
    BENGALS = "Bengals"
    TEXANS = "Texans"
    BUCCANEERS = "Buccaneers"

class GameBase(SQLModel):
    week: int = Field(index=True, ge=1, le=22)
    home_team: NflTeam
    away_team: NflTeam
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)

class Game(GameBase, table=True):
    id: UUID = PkField()

    coin_flips: list["CoinFlip"] = Relationship(back_populates="game", cascade_delete=True)

class CreateGame(GameBase):
    pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# User
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class League(str, Enum):
    LOWER = "lower"
    UPPER = "upper"

class User(SQLModel, table=True):
    id: UUID = PkField()

    name: str
    league: League
    coin_flip_bets: list["CoinFlipBet"] = Relationship(back_populates="user", cascade_delete=True)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CoinFlip
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CoinFlipSide(str, Enum):
    HEADS = "heads"
    TAILS = "tails"

class CoinFlip(SQLModel, table=True):
    id: UUID = PkField()

    game_id: UUID = Field(index=True, foreign_key="game.id", ondelete="CASCADE")
    game: Game = Relationship(back_populates="coin_flips")

    bets: list["CoinFlipBet"] = Relationship(back_populates="coin_flip", cascade_delete=True)

    winning_side: CoinFlipSide | None = None

class CoinFlipBet(SQLModel, table=True):
    id: UUID = PkField()

    user_id: UUID = Field(index=True, foreign_key="user.id", ondelete="CASCADE")
    user: User = Relationship(back_populates="coin_flip_bets")

    coin_flip_id: UUID = Field(index=True, foreign_key="coinflip.id", ondelete="CASCADE")
    coin_flip: CoinFlip = Relationship(back_populates="bets")

    side: CoinFlipSide
    amount: int = Field(gt=0)

