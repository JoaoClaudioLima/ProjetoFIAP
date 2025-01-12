from alembic import command
from alembic.config import Config
import uvicorn
from fastapi import FastAPI

from src.controller.routes import router
from src.settings import Settings


# Executa as migrações do Alembic.
alembic_cfg = Config("alembic.ini")

# Faz com que toda vez que o container é gerado, crie uma db nova. Comentar a linha 14 para que os dados persistam.
command.downgrade(alembic_cfg, "base")

command.upgrade(alembic_cfg, "head")

app = FastAPI(
    title="API projeto do board de tarefas - FIAP",
    description="API para o Board de Tarefa -> Melhorar descrição",
    version=Settings.VERSION,
    redoc_url=f"/apis/partner-redoc",
    openapi_url=f"/apis/partner/openapi.json",
)

api_prefix = "/api/v1"

app.include_router(router=router, prefix=api_prefix, tags=["FIAP"])


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8123,
    )
