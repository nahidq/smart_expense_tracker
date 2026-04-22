import os
from datetime import timedelta, timezone, datetime
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.repositories.user_repository import UserRepository
from app.database.db import get_db



load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES =  int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def hash_password(password: str) -> str:
    print("HASH_PASSWORD type:", type(password))
    print("HASH_PASSWORD repr:", repr(password))
    print("HASH_PASSWORD len:", len(password))
    print("HASH_PASSWORD bytes:", len(password.encode("utf-8")))
    return pwd_context.hash(password)

    # return pwd_context.hash(password)

def verify_password(input_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(input_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta| None= None) -> str:

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt  = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


    user = UserRepository.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user


