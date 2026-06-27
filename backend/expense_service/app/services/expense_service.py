from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.expense_schemas import ExpenseCreate, ExpenseUpdate
from app.repositories.expense_repository import ExpenseRepository
from app.exceptions.expense_exceptions import ExpenseNotFound
from app.models.expense import Expense


class ExpenseService:
    """Business logic + transaction boundaries. Composes the repository and
    decides when a unit of work commits or rolls back."""

    @staticmethod
    def create_expense(db: Session, data: ExpenseCreate, user_id: int) -> Expense:
        expense = Expense(**data.model_dump(), user_id=user_id)
        try:
            ExpenseRepository.add(db, expense)
            db.commit()
            db.refresh(expense)
            return expense
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_expense(db: Session, expense_id: int, user_id: int) -> Expense:
        expense = ExpenseRepository.get(db, expense_id, user_id)
        if not expense:
            raise ExpenseNotFound()
        return expense

    @staticmethod
    def list_expenses(
        db: Session,
        user_id: int,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Expense], int]:
        return ExpenseRepository.list(
            db, user_id, category, start_date, end_date, limit, offset
        )

    @staticmethod
    def update_expense(db: Session, expense_id: int, data: ExpenseUpdate, user_id: int) -> Expense:
        expense = ExpenseRepository.get(db, expense_id, user_id)
        if not expense:
            raise ExpenseNotFound()

        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            setattr(expense, key, value)

        try:
            db.commit()
            db.refresh(expense)
            return expense
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete_expense(db: Session, expense_id: int, user_id: int) -> None:
        expense = ExpenseRepository.get(db, expense_id, user_id)
        if not expense:
            raise ExpenseNotFound()
        try:
            ExpenseRepository.delete(db, expense)
            db.commit()
        except Exception:
            db.rollback()
            raise
