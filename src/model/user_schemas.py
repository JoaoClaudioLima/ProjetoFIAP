from pydantic import BaseModel, Field, StrictStr
from pydantic import field_validator

from src.utils.database import *


# CREATE class
class UserInput(BaseModel):
    '''
    Class responsible for handling user input.
    '''
    username: StrictStr = Field(default=None, description="User username", example="joao.lima")
    email: StrictStr = Field(default=None, description="User email", example="j.lima@fakemail.com")
    full_name: StrictStr = Field(default=None, description="User full name", example="João Lima")
    password: StrictStr = Field(default=None, description="User password", example="joao_lima_FAKE_password123!")

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


# DELETE and PUT classes
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


# PATCH classes
class UserUpdateFull(BaseModel):
    username: str
    email: str
    full_name: str
    password: str


class UserUpdateFullInput(BaseModel):
    authentication: UserAuthentication
    to_update: UserUpdateFull
