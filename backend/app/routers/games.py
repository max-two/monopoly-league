from fastapi import APIRouter
from sqlmodel import select
from ..dependencies import DB
from ..models.game import CreateGame, Game, ReadGame


router = APIRouter(
    prefix="/games",
)

@router.post("")
async def create_game(db: DB, game: CreateGame) -> ReadGame:
    db_game = Game.model_validate(game)

    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


@router.get("")
async def games(db: DB) -> list[ReadGame]:
    statement = select(Game)
    games = db.exec(statement).all()
    
    # Convert each result to a Game object
    return games
