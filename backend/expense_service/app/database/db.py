from dotenv import  load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker, DeclarativeBase
import  os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR/".env", override=False)
DATABASE_URL = os.getenv("EXPENSE_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("EXPENSE_DATABASE_URL is not set")

# echo is opt-in via env so production logs aren't flooded with SQL.
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"
engine = create_engine(DATABASE_URL, echo=SQL_ECHO)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
# Creating session per request
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


