
from sqlalchemy.orm import Session
from app.models.expense import Expense

class ExpenseRepository:
    @staticmethod
    def create_expense(db: Session, expense: Expense, user_id: int)-> Expense:
        new_expense = Expense(**expense.model_dump(), user_id=user_id)
        try:
            db.add(new_expense)
            db.commit()
            db.refresh(new_expense)
            return new_expense
        except:
            db.rollback()
            raise

    @staticmethod
    def get_expense(db: Session, expense_id: int , user_id: int) -> Expense | None:

        return db.query(Expense).filter(
            Expense.id == expense_id ,
            Expense.user_id == user_id
         ).first()

    @staticmethod
    def get_expenses(db: Session, user_id: int) -> list[Expense]:

        return db.query(Expense).filter(Expense.user_id == user_id).all()

    @staticmethod
    def update_expense(db: Session, expense_id: int , expense_update: Expense, user_id: int):

        expense = db.query(Expense).filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        ).first()

        if not expense:
            return None

        update_data = expense_update.model_dump(exclude_unset=True, exclude_none=True)

        for key, value in update_data.items():
                 setattr(expense,key,value)
        try:

            db.commit()
            db.refresh(expense)
            return expense
        except:
            db.rollback()
            raise

    @staticmethod
    def delete_expense(db: Session, expense_id: int, user_id: int) -> bool:

        expense = db.query(Expense).filter(
            Expense.id == expense_id,
                    Expense.user_id == user_id
                 ).first()
        if not expense:
            return False
        try:
            db.delete(expense)
            db.commit()
            return True
        except:
            db.rollback()
            raise