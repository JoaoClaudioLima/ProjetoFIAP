import uvicorn
from fastapi import FastAPI

from src.controller.routes import router
from src.settings import Settings

# Configuring latest database version via alembic
# alembicArgs = [
#     '--raiseerr',
#     'upgrade', 'head',
# ]
# alembic.config.main(argv=alembicArgs)

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
        port=8123,
    )
