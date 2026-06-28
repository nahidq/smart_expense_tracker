from dotenv import  load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker, DeclarativeBase
import  os

# Search upward for the nearest .env (the single root .env). In Docker there is
# no .env file and the env vars are injected directly, so this is a harmless no-op.
load_dotenv()
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


