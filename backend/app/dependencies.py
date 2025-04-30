from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from .db.db import get_session


# Create a new db session for each request
Sesh = Annotated[Session, Depends(get_session)]
