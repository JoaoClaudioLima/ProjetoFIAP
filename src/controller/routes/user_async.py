from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException, Query, APIRouter

from src.controller.user_celery import get_user_task
from celery.result import AsyncResult

v2_user_router = APIRouter()

@v2_user_router.get("/user_async/", response_model=None)
async def read_user(
    user_id: Optional[int] = Query(None, description="The ID of the user to retrieve"),
):
    try:
        task = get_user_task.apply_async(args=[user_id])
        result = AsyncResult(task)
        user_data = result.get(timeout=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a tarefa: {str(e)}")
    
    if not user_data:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado")
    
    return user_data
