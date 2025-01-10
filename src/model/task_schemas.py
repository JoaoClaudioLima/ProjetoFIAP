from typing import Union

from fastapi import HTTPException
from pydantic import BaseModel, Field, StrictStr, StrictInt, field_validator


# CREATE class
class TaskInput(BaseModel):
    '''
    Class responsible for handling task input.
    '''
    title: Union[str, None] = Field(description="Task title", example="Criação da classe de Input para as tarefas ")
    description: Union[str, None] = Field(description="Task description", example="Total imagine dream game again.")
    status_id: Union[int, None] = Field(default=1, description="Task status id", example=2)
    user_id: Union[int, None] = Field(default=None, description="Task user id", example=1)

    @field_validator('title')
    def title_must_exist(cls, v):
        if not v:
            raise HTTPException(400, 'A tarefa precisa ter um título')
        return v

    @field_validator('description')
    def description_must_exist(cls, v):
        if not v:
            raise HTTPException(400, 'A tarefa precisa ter uma descrição')
        return v


# UPDATE class
class TaskUpdateInput(BaseModel):
    '''
    Class responsible for handling task update input.
    '''
    title: Union[str, None] = Field(default=None, description="Task title", example="Criação da classe de Input para as tarefas ")
    description: Union[str, None] = Field(default=None, description="Task description", example="Total imagine dream game again.")
    status_id: Union[int, None] = Field(default=None, description="Task status id", example=2)
    user_id: Union[int, None] = Field(default=None, description="Task user id", example=1)
