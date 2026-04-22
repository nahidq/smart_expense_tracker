from app.database.db import Base
from sqlalchemy import Integer, String, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class User(Base):

    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key= True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)
    email: Mapped[str] = mapped_column(String,nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(20), nullable=True)
    hashed_password: Mapped[str]= mapped_column( VARCHAR(255), nullable=False)



