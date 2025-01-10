from typing import Union

from pydantic import BaseModel, Field, StrictStr, StrictInt


# CREATE class
class TaskInput(BaseModel):
    '''
    Class responsible for handling task input.
    '''
    task_id: Union[int, None] = Field(default=None, description="Task id", example=2)
    title: StrictStr = Field(default=None, description="Task title", example="Criação da classe de Input para as tarefas ")
    description: StrictStr = Field(default=None, description="Task description", example="Total imagine dream game again.")
    status_id: Union[int, None] = Field(default=None, description="Task status id", example=2)
    user_id: Union[int, None] = Field(default=None, description="Task user id", example=1)
