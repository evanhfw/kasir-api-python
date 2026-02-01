from fastapi import FastAPI

from kasir_api.handlers.category_handler import router as category_router
from kasir_api.handlers.health_handler import router as health_router

app = FastAPI()

app.include_router(category_router)
app.include_router(health_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
