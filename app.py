
import uvicorn
from fastapi import FastAPI

from ProjetoFIAP.src.controller import VERSION
from ProjetoFIAP.src.controller.routes import router

app = FastAPI(
    title="Temp",
    version=VERSION
)

api_prefix = "/api/v1"

app.include_router(router=router, prefix=api_prefix, tags=["users"])

if __name__ == "__main__":
    uvicorn.run(
        app,
        port=8123,
    )
