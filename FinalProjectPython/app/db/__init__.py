from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.params import Depends
from typing import Annotated

engine =create_engine("postgresql://postgres:4321@localhost:5432/finalproject-db")

LocalSession = sessionmaker(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

SessionContext = Annotated[Session, Depends(get_db)]