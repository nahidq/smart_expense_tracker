from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, hash_password
from app.exceptions.user_exceptions import InvalidCredentials, UserAlreadyExists
from app.schemas.user_schemas import UserCreate
from app.models.user import User


class UserService:

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)

        if not user:
            raise InvalidCredentials()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentials()

        return user

    @staticmethod
    def register_user(db: Session, user: UserCreate):
        existing_user = UserRepository.get_by_email(db, user.email)
        if existing_user:
            raise UserAlreadyExists()

        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hash_password(user.password),
        )
        try:
            UserRepository.add(db, new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception:
            db.rollback()
            raise
