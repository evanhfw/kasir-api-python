from kasir_api.models.product import Product, CreateProductRequest, UpdateProductRequest
from kasir_api.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_all(self) -> list[Product]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Product:
        return await self.repository.get_by_id(id)

    async def create(self, request: CreateProductRequest) -> Product:
        product = Product(id=0, name=request.name, price=request.price, stock=request.stock, categoryid=request.categoryid)
        return await self.repository.create(product)

    async def update(self, id: int, request: UpdateProductRequest) -> Product:
        existing = await self.repository.get_by_id(id)
        updated = Product(
            id=existing.id,
            name=request.name if request.name is not None else existing.name,
            price=request.price if request.price is not None else existing.price,
            stock=request.stock if request.stock is not None else existing.stock,
            categoryid=request.categoryid if request.categoryid is not None else existing.categoryid,
        )
        return await self.repository.update(updated)

    async def delete(self, id: int) -> None:
        await self.repository.delete(id)