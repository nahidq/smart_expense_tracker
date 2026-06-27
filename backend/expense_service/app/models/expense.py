
from app.database.db import Base
from sqlalchemy import Integer, String, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import date, datetime, UTC



class Expense(Base):

    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    category: Mapped[str] = mapped_column(String(50), nullable=False, server_default="Other")

    date: Mapped[date] = mapped_column(Date, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


