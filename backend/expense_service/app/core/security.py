import os
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("ALGORITHM","HS256")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_identity(token: str = Depends(oauth2_scheme) ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY ,algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if  user_id is None:
            raise credentials_exception
    except JWTError:
        raise  credentials_exception

    return user_id



