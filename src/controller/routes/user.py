from typing import Optional

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from src.model.user_schemas import UserInput, UserUpdateInput, UserAuthentication
from src.utils.database import get_db, authenticate_user, check_email_exists, check_user_privileges, \
    check_username_availability, get_user_from_db
from src.utils.user import db_update_user, db_delete_user, db_read_user, db_create_user

v1_users_router = APIRouter()

@v1_users_router.post("/user/login/", response_model=None, status_code=200,
                   responses={
                       200: {
                           "description": "Successful Response",
                           "content": {
                               "application/json": {
                                   "example": {
                                       "user_id": 1
                                   }
                               }
                           }
                       },
                       400: {
                           "description": "Error: Bad Request",
                           "content": {
                               "application/json": {
                                   "example": {
                                       "detail": "Email ou senha incorretos."
                                   }
                               }
                           }
                       }
                   }
                   )
def login_user(user: UserAuthentication, db: Session = Depends(get_db)):
    """
    Realiza o login de um usuário e retorna seu ID.

    Payload:
    - **email**: Email do usuário, deve ser único. (string)
    - **password**: Senha do usuário. (string)
    """
    authenticate_user(db, user.email, user.password)
    data = get_user_from_db(db=db, email=user.email)
    response = {
        "user_id": data,
    }
    return response


@v1_users_router.post("/user/", response_model=None, status_code=201,
                   responses={
                       201: {
                           "description": "Successful Response",
                           "content": {
                               "application/json": {
                                   "example": "Usuário criado."
                               }
                           }
                       },
                       400: {
                           "description": "Error: Bad Request",
                           "content": {
                               "application/json": {
                                   "example": {
                                       "detail": "Nome de usuário já está em uso."
                                   }
                               }
                           }
                       }
                   }
                   )
def create_user(user: UserInput, db: Session = Depends(get_db)):
    """
    Cria um novo usuário. O endpoint possui restrições para cadastros com usuários, emails já em uso, bem como validação de senha.

    Payload:
    - **username**: Apelido do usuário. (string)
    - **email**: Email do usuário, deve ser único. (string)
    - **full_name**: Nome completo do usuário. (string)
    - **password**: Senha do usuário. (string)
    """
    db_create_user(user, db)
    return "Usuário criado."


@v1_users_router.get("/user/", response_model=None,
                  responses={
                      200: {
                          "description": "Successful Response",
                          "content": {
                              "application/json": {
                                  "example": [
                                      {
                                          "is_admin": True,
                                          "username": "j.lima",
                                          "full_name": "Joao Lima",
                                          "created_at": "2025-01-17T02:59:39.254411",
                                          "deleted_at": None,
                                          "id": 1,
                                          "email": "joao.lima@fakemail.com",
                                          "hashed_password": "$2b$12$eYglZHp2AaJv6KjCrabXq.vknwRyeC0mnX.7YC9e2Qv.IBlkBENc6",
                                          "updated_at": "2025-01-17T02:59:39.254411"
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
def read_user(user_id: Optional[int] = Query(None,
                                             description="ID do usuário a ser recuperado. Caso não seja informado, retorna todos os usuários."),
              db: Session = Depends(get_db)):
    """
    Lê as informações de um usuário específico ou de todos os usuários cadastrados.
    """
    task = db_read_user(db, user_id=user_id)
    if not task:
        raise HTTPException(400, "Usuário não encontrado.")
    return task


@v1_users_router.delete("/user/", response_model=None, status_code=200,
                     responses={
                         200: {
                             "description": "Successful Response",
                             "content": {
                                 "application/json": {
                                     "example": "Usuário deletado."
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
def delete_user(user: UserUpdateInput, db: Session = Depends(get_db)):
    """
    Atualiza para deletado o cadastro de um usuário específico.

    Deve ser informado um cadastro de autenticação, onde o usuário deve validar o login e pode apenas atualizar seu próprio cadastro. Usuários que sejam admins podem alterar qualquer cadastro.

    Também devem ser passadas informações do cadastro a ser deletado.

    Payload:
    - ***authentication***: Informações de autenticação (dict)
        - **email**: Email do usuário, deve ser único. (string)
        - **password**: Senha do usuário. (string)
    - ***to_update***: Informações de atualização (dict)
        - **email**: Email do usuário, deve ser único. (string)
        - **password**: Senha do usuário. (string)

    Quando o usuário for deletado ele será removido do board de tarefas. Caso possua alguma tarefa atribuída, esta ficará sem responsável.
    """
    authenticate_user(db, user.authentication.email, user.authentication.password)
    check_user_privileges(db, user.authentication.email, user.to_update.email)
    task = db_delete_user(db, user=user)

    if not task:
        raise HTTPException(400, "Usuário não encontrado.")
    return "Usuário deletado."


@v1_users_router.put("/user/", response_model=None,
                  responses={
                      200: {
                          "description": "Successful Response",
                          "content": {
                              "application/json": {
                                  "example": "Usuário atualizado."
                              }
                          }
                      },
                      400: {
                          "description": "Error: Bad Request",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "detail": "Email de autenticação não encontrado."
                                  }
                              }
                          }
                      }
                  }
                  )
def update_user(user: UserUpdateInput, db: Session = Depends(get_db)):
    """
    Atualiza o cadastro de um usuário específico.

    Deve ser informado um cadastro de autenticação, onde o usuário deve validar o login e pode apenas atualizar seu próprio cadastro. Usuários que sejam admins podem alterar qualquer cadastro.

    Também deve ser passadas informações a serem atualizadas. O email nunca poderá ser atualizado. Os outros parâmetros podem ser enviados individualmente ou em conjunto.

    Payload:
    - ***authentication***: Informações de autenticação (dict)
        - **email**: Email do usuário, deve ser único. (string)
        - **password**: Senha do usuário. (string)
    - ***to_update***: Informações de atualização (dict)
        - **username**: Apelido do usuário. (string)
        - **email**: Email do usuário, deve ser único. (string)
        - **full_name**: Nome completo do usuário. (string)
        - **password**: Senha do usuário. (string)

    """
    if not check_email_exists(db, user.authentication.email):
        raise HTTPException(400, "Email de autenticação não encontrado.")

    if user.authentication.email != user.to_update.email:
        if not check_email_exists(db, user.to_update.email):
            raise HTTPException(400, "Email para atualização não encontrado.")

    check_username_availability(db, user.to_update.username)
    authenticate_user(db, user.authentication.email, user.authentication.password)
    check_user_privileges(db, user.authentication.email, user.to_update.email)

    task = db_update_user(db=db, user=user)

    if not task:
        raise HTTPException(400, "Usuário não pôde ser atualizado.")
    return "Usuário atualizado."
