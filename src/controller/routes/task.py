from typing import Optional

from fastapi import Depends, Query, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.model.task_schemas import TaskInput, TaskUpdateInput
from src.utils.database import get_db
from src.utils.task import db_create_task, db_read_task, db_delete_task, db_update_task

tasks_router = APIRouter()


@tasks_router.post("/tasks/", response_model=None, status_code=201,
                   responses={
                       201: {
                           "description": "Successful Response",
                           "content": {
                               "application/json": {
                                   "example": "Tarefa criada."
                               }
                           }
                       },
                       400: {
                           "description": "Error: Bad Request",
                           "content": {
                               "application/json": {
                                   "example": {
                                       "detail": "Usuário não encontrado."
                                   }
                               }
                           }
                       }
                   }
                   )
def create_task(task: TaskInput, db: Session = Depends(get_db)):
    """
    Cria uma nova tarefa.

    Payload:
    - **title**: Título da tarefa. (string)
    - **description**: Descrição da tarefa. (string)
    - **status_id**: ID do status da tarefa. Opcional, mas se for enviado deve existir no cadastro de status de tarefas. (integer)
    - **user_id**: ID do usuário. Opcional, mas se for enviado deve existir no cadastro de usuários.(integer)
    """
    db_create_task(task, db)
    return "Tarefa criada."


@tasks_router.get("/tasks/", response_model=None,
                  responses={
                      200: {
                          "description": "Successful Response",
                          "content": {
                              "application/json": {
                                  "example": [
                                      {
                                          "description": "Matter school soon address draw myself state.",
                                          "status_id": 3,
                                          "created_at": "2025-01-17T04:17:33.073530",
                                          "deleted_at": None,
                                          "title": "Tarefa 1",
                                          "id": 1,
                                          "user_id": 8,
                                          "updated_at": "2025-01-17T04:17:33.073530"
                                      }
                                  ]
                              }
                          }
                      },
                      400: {
                          "description": "Error: Bad Request",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "detail": "Usuário não encontrado."
                                  }
                              }
                          }
                      }
                  }
                  )
def read_task(
        user_id: Optional[int] = Query(None,
                                       description="ID do usuário. Retorna todas as tarefas que o usuário possui."),
        status_id: Optional[int] = Query(None,
                                         description="ID do status da tarefa. Retorna todas as tarefas com esse status."),
        task_id: Optional[int] = Query(None, description="ID da tarefa."),
        db: Session = Depends(get_db)
):
    """
    Lê tarefas válidas com base nos parâmetros enviados.
    """
    if any([user_id, status_id, task_id]):
        task = db_read_task(db=db, user_id=user_id, status_id=status_id, task_id=task_id)
        return task

    tasks = db_read_task(db=db)
    return tasks


@tasks_router.delete("/tasks/", response_model=None, status_code=200,
                     responses={
                         200: {
                             "description": "Successful Response",
                             "content": {
                                 "application/json": {
                                     "example": "Tarefa deletada."
                                 }
                             }
                         },
                         400: {
                             "description": "Error: Bad Request",
                             "content": {
                                 "application/json": {
                                     "example": {
                                         "detail": "Tarefa não encontrada."
                                     }
                                 }
                             }
                         }
                     }
                     )
def delete_task(
        task_id: Optional[int] = Query(None, description="ID da tarefa a ser deletada."),
        db: Session = Depends(get_db)):
    """
    Deleta uma tarefa.
    """
    task = db_delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=400, detail="Tarefa não encontrada.")
    return "Tarefa deletada."


@tasks_router.put("/tasks/", response_model=None, status_code=200,
                  responses={
                      200: {
                          "description": "Successful Response",
                          "content": {
                              "application/json": {
                                  "example": "Tarefa atualizada."
                              }
                          }
                      },
                      400: {
                          "description": "Error: Bad Request",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "detail": "Tarefa não pôde ser atualizada."
                                  }
                              }
                          }
                      }
                  })
def update_task(
        task: TaskUpdateInput,
        task_id: str = Query(None, description="ID da tarefa a ser atualizada."),
        remove_user: bool = Query(False,
                                  description="Remove o usuário da tarefa. Caso seja passado como True, ignora o payload enviado."),
        db: Session = Depends(get_db)):
    """
    Atualiza a tarefa tarefa com base nos parâmetros enviados.

    Payload:
    - **title**: Título da tarefa. Opcional.(string)
    - **description**: Descrição da tarefa. Opcional.(string)
    - **status_id**: ID do status da tarefa. Opcional, mas se for enviado deve existir no cadastro de status de tarefas. (integer)
    - **user_id**: ID do usuário. Opcional, mas se for enviado deve existir no cadastro de usuários.(integer)
    """

    if not task_id:
        raise HTTPException(status_code=400, detail="ID da tarefa não encontrado.")

    task = db_update_task(db=db, task_input=task, task_id=task_id, remove_user=remove_user)

    if not task:
        raise HTTPException(status_code=400, detail="Tarefa não pôde ser atualizada.")
    return "Tarefa atualizada"
