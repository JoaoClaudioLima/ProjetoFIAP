from alembic import command
from alembic.config import Config
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    docs_url=f"/apis/partner-docs",  # Adiciona o caminho do Swagger UI
    redoc_url=f"/apis/partner-redoc",
    openapi_url=f"/apis/partner/openapi.json",
)

api_prefix = "/api/v1"

app.include_router(router=router, prefix=api_prefix, tags=["FIAP"])


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8123",
    "http://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8123,
    )
