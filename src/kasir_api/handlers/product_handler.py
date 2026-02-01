from fastapi import APIRouter, Depends, HTTPException

from kasir_api.errors import NotFoundError, ConflictError
from kasir_api.models.product import Product, CreateProductRequest, UpdateProductRequest
from kasir_api.repositories.db import pool
from kasir_api.repositories.product_repository import ProductRepository
from kasir_api.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])

def get_service() -> ProductService:
    repository = ProductRepository(pool)
    return ProductService(repository)

@router.get("", response_model=list[Product])
async def get_all(service: ProductService = Depends(get_service)):
    return await service.get_all()

@router.get("/{id}", response_model=Product)
async def get_by_id(id: int, service: ProductService = Depends(get_service)):
    try:
        return await service.get_by_id(id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.post("", response_model=Product, status_code=201)
async def create(
    request: CreateProductRequest,
    service: ProductService = Depends(get_service),
):
    try:
        return await service.create(request)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)
    
@router.put("/{id}", response_model=Product)
async def update(
    id: int,
    request: UpdateProductRequest,
    service: ProductService = Depends(get_service),
):
    try:
        return await service.update(id, request)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@router.delete("/{id}", status_code=204)
async def delete(id: int, service: ProductService = Depends(get_service)):
    try:
        await service.delete(id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)