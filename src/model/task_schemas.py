from pydantic import BaseModel, Field, StrictStr, StrictInt


# CREATE class
class TaskInput(BaseModel):
    '''
    Class responsible for handling task input.
    '''
    title: StrictStr = Field(default=None, description="Task title", example="Criação da classe de Input para as tarefas ")
    description: StrictStr = Field(default=None, description="Task description", example="Total imagine dream game again.")
    status_id: StrictInt = Field(default=1, description="Task status id", example=2)
    user_id: int = Field(default=None, description="Task user id", example=1)
