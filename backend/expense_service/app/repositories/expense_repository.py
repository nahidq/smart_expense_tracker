from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from app.models.expense import Expense


class ExpenseRepository:
    """Pure data access. No transaction control (commit/rollback) lives here —
    that is the service layer's job."""

    @staticmethod
    def add(db: Session, expense: Expense) -> Expense:
        db.add(expense)
        db.flush()  # sends the INSERT so expense.id is populated, still inside the txn
        return expense

    @staticmethod
    def get(db: Session, expense_id: int, user_id: int) -> Expense | None:
        return db.query(Expense).filter(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        ).first()

    @staticmethod
    def list( db: Session, user_id: int, category: Optional[str] = None, start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Expense], int]:

        query = db.query(Expense).filter(Expense.user_id == user_id)

        if category is not None:
            query = query.filter(Expense.category == category)
        if start_date is not None:
            query = query.filter(Expense.date >= start_date)
        if end_date is not None:
            query = query.filter(Expense.date <= end_date)

        # Count the full result set BEFORE paginating.
        total = query.count()

        items = (
            query.order_by(Expense.date.desc(), Expense.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return items, total

    @staticmethod
    def delete(db: Session, expense: Expense) -> None:
        db.delete(expense)
