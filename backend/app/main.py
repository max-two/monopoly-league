from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query

from app.models.game import Game


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/games")
async def create_game(game: Game, session: SessionDep) -> Game:
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@app.get("/games")
async def games(session: SessionDep) -> list[Game]:
    statement = select(Game)
    results = session.exec(statement).all()

    return results
