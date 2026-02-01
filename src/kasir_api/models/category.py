from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    description: str | None = None


class CreateCategoryRequest(BaseModel):
    name: str
    description: str | None = None


class UpdateCategoryRequest(BaseModel):
    name: str | None = None
    description: str | None = None
