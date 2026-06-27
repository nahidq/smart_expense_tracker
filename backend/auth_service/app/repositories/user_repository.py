from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    """Pure data access. Transaction control (commit/rollback) lives in the
    service layer, not here."""

    @staticmethod
    def add(db: Session, user: User) -> User:
        db.add(user)
        db.flush()  # populates user.user_id without committing
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: EmailStr) -> User | None:
        return db.query(User).filter(User.email == email).first()
