from fastapi import FastAPI, APIRouter

from kasir_api.handlers.category_handler import router as category_router
from kasir_api.handlers.health_handler import router as health_router
from kasir_api.handlers.product_handler import router as product_router
from kasir_api.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix="/api")
api_router.include_router(category_router)
api_router.include_router(health_router)
api_router.include_router(product_router)

app.include_router(api_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
