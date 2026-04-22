from pydantic import BaseModel
from typing import Optional
from datetime import date as dt_date, datetime


class ExpenseBase(BaseModel):
    title: str
    description: Optional[str] = None
    amount: float
    date: dt_date

class ExpenseCreate(ExpenseBase):
        pass

class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[dt_date] = None

class ExpenseResponse(ExpenseBase):

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes ": True}