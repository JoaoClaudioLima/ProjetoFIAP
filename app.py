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
    title="Temp",
    version=Settings.VERSION,
)

api_prefix = "/api/v1"

app.include_router(router=router, prefix=api_prefix, tags=["FIAP"])


if __name__ == "__main__":
    uvicorn.run(
        app,
        port=8123,
    )
