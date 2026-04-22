
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
from sqlalchemy.orm  import Session
from app.schemas.user_schemas import UserCreate, UserResponse
from app.database.db import get_db
from app.repositories.user_repository import UserRepository
from app.exceptions.user_exceptions import UserAlreadyExists
from app.core.security import get_current_user
from app.models.user import User
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags= ["Users"])

@router.post("/", status_code=201, response_model= UserResponse)
def create_user(user:UserCreate, db: Session= Depends(get_db)):
    print("Password length:", len(user.password))
    print("Password bytes:", len(user.password.encode("utf-8")))
    try:
        created_user = UserService.register_user(db, user)
        return created_user

    except UserAlreadyExists:
        raise HTTPException(status_code=409, detail="Email already exists")


@router.get("/by-email", response_model= UserResponse)
def get_user_by_email(
        email: EmailStr=Query(...),
        db: Session= Depends(get_db)
):

    user= UserRepository.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


