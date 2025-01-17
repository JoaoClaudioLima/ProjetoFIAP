from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.model.database import TaskStatus
from src.utils.database import get_from_db, get_db

task_status_router = APIRouter()


@task_status_router.get("/task-status/", response_model=None,
                        responses={
                            200: {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "example": [
                                            {
                                                "id": 1,
                                                "name": "To Do"
                                            }
                                        ]
                                    }
                                }
                            },
                        }
                        )
def read_task_status(db: Session = Depends(get_db)):
    """
    Lê as informações de status de tarefas cadastrados.
    """
    task_status = get_from_db(TaskStatus, db)
    return task_status
