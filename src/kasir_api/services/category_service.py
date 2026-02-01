from kasir_api.models.category import Category, CreateCategoryRequest, UpdateCategoryRequest
from kasir_api.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def get_all(self) -> list[Category]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Category:
        return await self.repository.get_by_id(id)

    async def create(self, request: CreateCategoryRequest) -> Category:
        category = Category(id=0, name=request.name, description=request.description)
        return await self.repository.create(category)

    async def update(self, id: int, request: UpdateCategoryRequest) -> Category:
        existing = await self.repository.get_by_id(id)
        updated = Category(
            id=existing.id,
            name=request.name if request.name is not None else existing.name,
            description=request.description if request.description is not None else existing.description,
        )
        return await self.repository.update(updated)

    async def delete(self, id: int) -> None:
        await self.repository.delete(id)
