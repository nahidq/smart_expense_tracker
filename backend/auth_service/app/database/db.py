from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

import os

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("USER_DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL, echo= True)

SessionLocal = sessionmaker(bind=engine, autoflush= False,autocommit = False)
class Base(DeclarativeBase):
    pass

def get_db():

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()


