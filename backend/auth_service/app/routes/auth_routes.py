
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schemas import Token, UserLogin
from sqlalchemy.orm  import Session
from app.database.db import get_db
from app.repositories.user_repository import UserRepository
from app.core.security import create_access_token, verify_password
from app.services.user_service import UserService
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions.user_exceptions import InvalidCredentials

router = APIRouter(prefix="/auth" , tags=["Authentication"])


@router.post("/token", response_model=Token)
def login_for_docs(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.user_id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login",response_model=Token,status_code=status.HTTP_200_OK )
def login(user_data: UserLogin, db : Session = Depends(get_db)):

    try:
        user = UserService.authenticate_user(db, user_data.email, user_data.password)

    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data = {"sub": user.email, "user_id": user.user_id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


