from enum import Enum
from uuid import uuid4, UUID

from sqlmodel import Field, Relationship, SQLModel

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

def PkField():
    return Field(default_factory=uuid4, primary_key=True)


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
    over_under_bets: list["OverUnderBet"] = Relationship(back_populates="user", cascade_delete=True)
    spread_bets: list["SpreadBet"] = Relationship(back_populates="user", cascade_delete=True)

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
    over_unders: list["OverUnder"] = Relationship(back_populates="game", cascade_delete=True)
    spreads: list["Spread"] = Relationship(back_populates="game", cascade_delete=True)

class CreateGame(GameBase):
    pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CoinFlip
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CoinFlipSide(str, Enum):
    HEADS = "heads"
    TAILS = "tails"

class CoinFlip(SQLModel, table=True):
    id: UUID = PkField()

    winning_side: CoinFlipSide | None = None

    game_id: UUID = Field(index=True, foreign_key="game.id", ondelete="CASCADE")
    game: Game = Relationship(back_populates="coin_flips")

    bets: list["CoinFlipBet"] = Relationship(back_populates="coin_flip", cascade_delete=True)

class CoinFlipBet(SQLModel, table=True):
    id: UUID = PkField()

    side: CoinFlipSide
    amount: int = Field(gt=0)

    user_id: UUID = Field(index=True, foreign_key="user.id", ondelete="CASCADE")
    user: User = Relationship(back_populates="coin_flip_bets")

    coin_flip_id: UUID = Field(index=True, foreign_key="coinflip.id", ondelete="CASCADE")
    coin_flip: CoinFlip = Relationship(back_populates="bets")



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OverUnder
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OverUnderSide(str, Enum):
    OVER = "over"
    UNDER = "under"

class OverUnder(SQLModel, table=True):
    id: UUID = PkField()

    line: float = Field(ge=0)

    game_id: UUID = Field(index=True, foreign_key="game.id", ondelete="CASCADE")
    game: Game = Relationship(back_populates="over_unders")

    bets: list["OverUnderBet"] = Relationship(back_populates="over_under", cascade_delete=True)

class OverUnderBet(SQLModel, table=True):
    id: UUID = PkField()

    side: OverUnderSide
    amount: int = Field(gt=0)

    user_id: UUID = Field(index=True, foreign_key="user.id", ondelete="CASCADE")
    user: User = Relationship(back_populates="over_under_bets")

    over_under_id: UUID = Field(index=True, foreign_key="overunder.id", ondelete="CASCADE")
    over_under: OverUnder = Relationship(back_populates="bets")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Spread
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SpreadSide(str, Enum):
    HOME = "home"
    AWAY = "away"

class Spread(SQLModel, table=True):
    id: UUID = PkField()

    line: float # Always references home team

    game_id: UUID = Field(index=True, foreign_key="game.id", ondelete="CASCADE")
    game: Game = Relationship(back_populates="spreads")

    bets: list["SpreadBet"] = Relationship(back_populates="spread", cascade_delete=True)

class SpreadBet(SQLModel, table=True):
    id: UUID = PkField()

    side: SpreadSide
    amount: int = Field(gt=0)

    user_id: UUID = Field(index=True, foreign_key="user.id", ondelete="CASCADE")
    user: User = Relationship(back_populates="spread_bets")

    spread_id: UUID = Field(index=True, foreign_key="spread.id", ondelete="CASCADE")
    spread: Spread = Relationship(back_populates="bets")



# The bet option to game relationship is actually one-to-one - therefore I should just get rid of them and make them columns?
# Can i add unique constraints to the columns?