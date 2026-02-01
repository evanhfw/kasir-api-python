from pydantic import BaseModel
from kasir_api.models.category import Category

class Product(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    categoryid: int
    category: Category | None = None