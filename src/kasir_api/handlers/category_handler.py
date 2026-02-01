from fastapi import APIRouter, Depends, HTTPException

from kasir_api.errors import NotFoundError, ConflictError
from kasir_api.models.category import Category, CreateCategoryRequest, UpdateCategoryRequest
from kasir_api.repositories.category_repository import CategoryRepository
from kasir_api.repositories.db import pool
from kasir_api.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


def get_service() -> CategoryService:
    repository = CategoryRepository(pool)
    return CategoryService(repository)


@router.get("", response_model=list[Category])
async def get_all(service: CategoryService = Depends(get_service)):
    return await service.get_all()


@router.get("/{id}", response_model=Category)
async def get_by_id(id: int, service: CategoryService = Depends(get_service)):
    try:
        return await service.get_by_id(id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("", response_model=Category, status_code=201)
async def create(
    request: CreateCategoryRequest,
    service: CategoryService = Depends(get_service),
):
    try:
        return await service.create(request)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.put("/{id}", response_model=Category)
async def update(
    id: int,
    request: UpdateCategoryRequest,
    service: CategoryService = Depends(get_service),
):
    try:
        return await service.update(id, request)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/{id}", status_code=204)
async def delete(id: int, service: CategoryService = Depends(get_service)):
    try:
        await service.delete(id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
