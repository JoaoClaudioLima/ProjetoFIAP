from pydantic import BaseModel, Field, StrictStr
from pydantic import field_validator

from src.utils.database import *


# CREATE class
class UserInput(BaseModel):
    """
    Classe responsável pela criação do Usuário.
    """
    username: StrictStr = Field(description="User username", example="joao.lima")
    email: StrictStr = Field(description="User email", example="j.lima@fakemail.com")
    full_name: StrictStr = Field(description="User full name", example="João Lima")
    password: StrictStr = Field(description="User password", example="joao_lima_FAKE_password123!")

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
            raise HTTPException(400, 'A senha deve ter mais de 8 caracteres')
        return v


# DELETE and PUT classes
class UserAuthentication(BaseModel):
    """
    Classe responsável pela autenticação do Usuário.
    """
    email: StrictStr = Field(description="User email", example="j.lima@fakemail.com")
    password: StrictStr = Field(description="User password", example="joao_lima_FAKE_password123!")


class UserUpdate(BaseModel):
    """
    Classe responsável pela atualização do Usuário.
    """
    username: StrictStr = Field(default=None, description="User username", example="joao.lima")
    email: StrictStr = Field(description="User email", example="j.lima@fakemail.com")
    full_name: StrictStr = Field(default=None, description="User full name", example="João Lima")
    password: StrictStr = Field(default=None, description="User password", example="joao_lima_FAKE_password123!")

    @field_validator("username")
    def username_must_be_unique(cls, v):
        validate_username_availability(v)
        return v

    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise HTTPException(400, 'A senha deve ter mais de 8 caracteres')
        return v


class UserUpdateInput(BaseModel):
    """
    Classe responsável pela atualização e autenticação do Usuário.
    """
    authentication: UserAuthentication
    to_update: UserUpdate
