from dotenv import  load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker, DeclarativeBase
import  os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR/".env", override=False)
DATABASE_URL = os.getenv("EXPENSE_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# Create engine
engine = create_engine(DATABASE_URL, echo= True)

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


