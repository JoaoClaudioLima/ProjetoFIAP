from pydantic import BaseModel
from pydantic import field_validator

from src.utils.database import *


# CREATE class
class UserInput(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

    @field_validator("email")
    def email_must_be_unique(cls, v):
        validate_email_availability(v)
        return v

    @field_validator("username")
    def username_must_be_unique(cls, v):
        validate_username_availability(v)
        return v

    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


# DELETE and PATCH classes
class UserAuthentication(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str = None
    email: str
    full_name: str = None
    password: str = None


class UserUpdateInput(BaseModel):
    authentication: UserAuthentication
    to_update: UserUpdate


# PUT classes
class UserUpdateFull(BaseModel):
    username: str
    email: str
    full_name: str
    password: str


class UserUpdateFullInput(BaseModel):
    authentication: UserAuthentication
    to_update: UserUpdateFull
