from typing import Union

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


# CREATE class
class TaskInput(BaseModel):
    """
    Classe responsável pela criação da Tarefa.
    """
    title: Union[str, None] = Field(description="Título da tarefa", example="Total imagine dream game again.")
    description: Union[str, None] = Field(description="Descrição da tarefa", example="Total imagine dream game again.")
    status_id: Union[int, None] = Field(default=1, description="ID do status da tarefa", example=2)
    user_id: Union[int, None] = Field(default=None, description="ID do usuário atribuído a tarefa", example=1)

    @field_validator("title")
    def title_must_exist(cls, v):
        if not v:
            raise HTTPException(400, "A tarefa precisa ter um título")
        return v

    @field_validator("description")
    def description_must_exist(cls, v):
        if not v:
            raise HTTPException(400, "A tarefa precisa ter uma descrição")
        return v


# PUT class
class TaskUpdateInput(BaseModel):
    """
    Classe responsável pela atualização da Tarefa.
    """
    title: Union[str, None] = Field(default=None, description="Título da tarefa", example="Total imagine dream game again.")
    description: Union[str, None] = Field(default=None, description="Descrição da tarefa", example="Total imagine dream game again.")
    status_id: Union[int, None] = Field(default=None, description="ID do status da tarefa", example=2)
    user_id: Union[int, None] = Field(default=None, description="ID do usuário atribuído a tarefa", example=1)
