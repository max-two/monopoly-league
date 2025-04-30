from fastapi import APIRouter
from sqlmodel import select
from ..dependencies import Sesh
from ..models.game import CreateGame, Game, ReadGame


router = APIRouter(
    prefix="/games",
)

@router.post("")
async def create_game(session: Sesh, game: CreateGame) -> ReadGame:
    db_game = Game.model_validate(game)

    session.add(db_game)
    session.commit()
    session.refresh(db_game)

    return db_game


@router.get("")
async def games(session: Sesh) -> list[ReadGame]:
    statement = select(Game)
    games = session.exec(statement).all()
    
    # Convert each result to a Game object
    return games
