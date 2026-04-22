from dataclasses import Field

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from pydantic import StringConstraints
from typing_extensions import Annotated


class UserBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr

class UserCreate(UserBase):

    first_name: str
    last_name: Optional[str] = None
    phone: Optional[
        Annotated[str, StringConstraints(pattern=r'^\+?\d{10,15}$')]
    ] = None
    email: EmailStr
    password: str

    # @field_validator("password")
    # @classmethod
    # def validate_password_length(cls, value):
    #     if len(value.encode("utf-8")) > 72:
    #         raise ValueError("Password must be at most 72 bytes")
    #     if len(value) < 6:
    #         raise ValueError("Password must be at least 6 characters")
    #     return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(UserBase):

     user_id: int
     model_config = {"from_attributes": True}


