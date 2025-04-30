from fastapi import APIRouter
from sqlmodel import select
from ..dependencies import Sesh
from ..models.game import Game


router = APIRouter(
    prefix="/games",
)

@router.post("/")
async def create_game(session: Sesh, game: Game) -> Game:
    session.add(game)
    session.commit()
    session.refresh(game)

    return game


@router.get("/")
async def games(session: Sesh) -> list[Game]:
    statement = select(Game)
    results = session.exec(statement).all()
    
    # Convert each result to a Game object
    return [Game.model_validate(result) for result in results]
