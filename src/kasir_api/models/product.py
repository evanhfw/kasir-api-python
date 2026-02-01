from pydantic import BaseModel
from kasir_api.models.category import Category

class Product(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    category_id: int
    category: Category | None = None

class CreateProductRequest(BaseModel):
    name: str
    price: int
    stock: int
    category_id: int

class UpdateProductRequest(BaseModel):
    name: str | None = None
    price: int | None = None
    stock: int | None = None
    category_id: int | None = None