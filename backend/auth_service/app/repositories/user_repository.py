
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.user import User
from app.exceptions.user_exceptions import UserNotFound


class UserRepository:

    @staticmethod
    def register_user(db: Session, new_user: User) -> User:

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except:
            db.rollback()
            raise

    @staticmethod
    def get_user_by_id(db: Session,user_id: int):
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise UserNotFound()

        return user

    @staticmethod
    def get_user_by_email(db: Session, email: EmailStr):
        return db.query(User).filter(User.email == email).first()


