from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

import os

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("USER_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("USER_DATABASE_URL is not set")

# echo is opt-in via env so production logs aren't flooded with SQL.
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"
engine = create_engine(DATABASE_URL, echo=SQL_ECHO)

SessionLocal = sessionmaker(bind=engine, autoflush= False,autocommit = False)
class Base(DeclarativeBase):
    pass

def get_db():

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()


