from dotenv import  load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker, DeclarativeBase
import  os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR/".env")
print(BASE_DIR)
# DATABASE_URL= "postgresql://postgres:8911@localhost:8911/expense_db"
DATABASE_URL = os.getenv("EXPENSE_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

print("DATABASE_URL =", DATABASE_URL)  # temporary debug
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


