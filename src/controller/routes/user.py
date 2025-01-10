from typing import Optional

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from src.model.user_schemas import UserInput, UserUpdateInput, UserAuthentication
from src.utils.database import get_db, authenticate_user, check_email_exists, check_user_privileges, \
    check_username_availability
from src.utils.user import db_update_user, db_delete_user, db_read_user, db_create_user

users_router = APIRouter()


@users_router.post("/user/login/", response_model=None, status_code=200)
def login_user(user: UserAuthentication, db: Session = Depends(get_db)):
    authenticate_user(db, user.email, user.password)
    return "OK"


@users_router.post("/user/", response_model=None, status_code=201)
def create_user(user: UserInput, db: Session = Depends(get_db)):
    db_create_user(user, db)
    return "Usuário criado"


@users_router.get("/user/", response_model=None)
def read_user(user_id: Optional[int] = Query(None, description="The ID of the user to retrieve"), db: Session = Depends(get_db)):
    task = db_read_user(db, user_id=user_id)
    if not task:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    return task


@users_router.delete("/user/", response_model=None, status_code=200)
def delete_user(user: UserUpdateInput, db: Session = Depends(get_db)):
    authenticate_user(db, user.authentication.email, user.authentication.password)
    check_user_privileges(db, user.authentication.email, user.to_update.email)
    task = db_delete_user(db, user=user)

    if not task:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return "Usuário deletado"


@users_router.put("/user/", response_model=None)
def update_user(user: UserUpdateInput, db: Session = Depends(get_db)):
    if not check_email_exists(db, user.authentication.email):
        raise HTTPException(status_code=400, detail="Email de autenticação não encontrado")

    if user.authentication.email != user.to_update.email:
        if not check_email_exists(db, user.to_update.email):
            raise HTTPException(status_code=400, detail="Email para atualização não encontrado")

    check_username_availability(db, user.to_update.username)
    authenticate_user(db, user.authentication.email, user.authentication.password)
    check_user_privileges(db, user.authentication.email, user.to_update.email)

    task = db_update_user(db=db, user=user)

    if not task:
        raise HTTPException(status_code=400, detail="Usuário não pôde ser atualizado")
    return "Usuário atualizado"  # TODO rever caso de mandar somente o email
