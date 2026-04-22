from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.expense_repository import ExpenseRepository
from app.database.db import get_db
from app.schemas.expense_schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.core.security import get_current_identity


router = APIRouter(prefix="/expenses",
                   tags= ["Expenses"])


@router.post("/",response_model= ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense:ExpenseCreate, db:Session= Depends(get_db), current_user_id: int = Depends(get_current_identity)):
    return ExpenseRepository.create_expense(db,expense,current_user_id)

@router.get("/{expense_id}", response_model= ExpenseResponse)
def get_expense(expense_id: int ,db: Session = Depends(get_db), current_user_id: int = Depends(get_current_identity)):

    expense = ExpenseRepository.get_expense(db, expense_id,current_user_id)

    if not expense:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Expense not found")

    return expense

@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session= Depends(get_db), current_user_id: int = Depends(get_current_identity)):

    updated_expense = ExpenseRepository.update_expense(db, expense_id, expense,current_user_id )
    if not updated_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Expense not found")

    return updated_expense



@router.delete("/{expense_id}")
def delete_expense(
        expense_id: int,
        db: Session=Depends(get_db),
        current_user_id: int = Depends(get_current_identity)
):
    success = ExpenseRepository.delete_expense(db, expense_id,current_user_id )
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Expense not found")

    return {"message": "Expense deleted successfully"}

@router.get("/", response_model=list[ExpenseResponse])
def list_expenses(db: Session = Depends(get_db),  current_user_id: int = Depends(get_current_identity)):
    return ExpenseRepository.get_expenses(db,current_user_id )