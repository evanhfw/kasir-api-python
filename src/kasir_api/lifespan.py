from contextlib import asynccontextmanager

from fastapi import FastAPI

from kasir_api.repositories.db import pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    yield
    await pool.close()
