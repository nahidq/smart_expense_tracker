from datetime import date
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.expense_schemas import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
    ExpenseCategory,
    ExpensePage,
)
from app.core.security import get_current_identity
from app.services.expense_service import ExpenseService
from app.exceptions.expense_exceptions import ExpenseNotFound


router = APIRouter(prefix="/expenses",
                   tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_identity)):
    return ExpenseService.create_expense(db, expense, current_user_id)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_identity)):
    try:
        return ExpenseService.get_expense(db, expense_id, current_user_id)
    except ExpenseNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_identity)):
    try:
        return ExpenseService.update_expense(db, expense_id, expense, current_user_id)
    except ExpenseNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_identity)):
    try:
        ExpenseService.delete_expense(db, expense_id, current_user_id)
    except ExpenseNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return {"message": "Expense deleted successfully"}


@router.get("/", response_model=ExpensePage)
def list_expenses(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_identity),
    category: Optional[ExpenseCategory] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    items, total = ExpenseService.list_expenses(
        db,
        current_user_id,
        category=category,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}
