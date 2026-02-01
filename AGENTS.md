# AGENTS.md - Kasir API Python

Guidelines for AI agents working in this codebase.

## Project Overview

A Point of Sale (Kasir) REST API built with FastAPI and PostgreSQL.

- **Language**: Python 3.14+
- **Framework**: FastAPI
- **Database**: PostgreSQL via psycopg (async)
- **Package Manager**: uv
- **Models**: Pydantic BaseModel

## Build & Run Commands

```bash
# Install dependencies
uv sync

# Run development server
uv run fastapi dev src/kasir_api/app.py

# Run production server
uv run fastapi run src/kasir_api/app.py --port 8000
```

## Testing Commands

```bash
# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_example.py

# Run a specific test function
uv run pytest tests/test_example.py::test_function_name

# Run tests with verbose output
uv run pytest -v

# Run tests matching a pattern
uv run pytest -k "test_category"

# Run with coverage
uv run pytest --cov=src/kasir_api
```

## Linting & Formatting

No linter/formatter is currently configured. Recommended tools:

```bash
# If ruff is added:
uv run ruff check src/
uv run ruff format src/

# If mypy is added:
uv run mypy src/
```

## Project Structure

```
src/kasir_api/
├── app.py                    # FastAPI application entry point
├── config.py                 # Environment variable loading
├── settings.py               # Settings class
├── errors.py                 # Custom exception classes
├── models/                   # Pydantic models
│   ├── category.py
│   └── product.py
├── repositories/             # Database access layer
│   ├── db.py                 # Connection pool
│   ├── category_repository.py
│   └── product_repository.py
└── handlers/                 # Request handlers (currently empty)
```

## Code Style Guidelines

### Imports

Order imports in this sequence, separated by blank lines:
1. Standard library
2. Third-party packages
3. Local application imports

```python
import os

from fastapi import FastAPI
from pydantic import BaseModel

from kasir_api.config import DATABASE_URL
from kasir_api.models.category import Category
```

### Type Annotations

- Always use type hints for function parameters and return values
- Use modern union syntax: `str | None` (not `Optional[str]`)
- Use `list[T]` instead of `List[T]`

```python
async def get_by_id(self, id: int) -> Category | None:
    ...

async def get_all(self) -> list[Category]:
    ...
```

### Naming Conventions

- **Classes**: PascalCase (`CategoryRepository`, `Product`)
- **Functions/Methods**: snake_case (`get_by_id`, `find_all`)
- **Variables**: snake_case (`database_url`, `row_factory`)
- **Constants**: UPPER_SNAKE_CASE (`DATABASE_URL`, `PORT`)
- **Files**: snake_case (`category_repository.py`)

### Pydantic Models

Define models in `src/kasir_api/models/` directory:

```python
from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str
    description: str | None = None
```

### Repository Pattern

Database access follows the repository pattern in `src/kasir_api/repositories/`:

```python
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

class CategoryRepository:
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    @staticmethod
    def _to_model(row: dict) -> Category:
        return Category(**row)

    async def get_all(self) -> list[Category]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    SELECT id, name, description
                    FROM categories
                """)
                rows = await cur.fetchall()
        return [self._to_model(r) for r in rows]
```

### Error Handling

Use custom exceptions from `src/kasir_api/errors.py`:

```python
from kasir_api.errors import NotFoundError, ConflictError, ValidationError

# Available exceptions:
# - AppError: Base class for all app errors
# - NotFoundError: Resource not found (404)
# - ConflictError: Data conflict/unique constraint (409)
# - ValidationError: Invalid data (400)
# - UnauthorizedError: No access (401)
```

### Async/Await

All database operations and handlers should be async:

```python
async def create(self, category: Category) -> Category:
    async with self.pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(...)
```

### SQL Queries

- Use triple-quoted strings for multi-line SQL
- Use parameterized queries with `%s` placeholders (psycopg style)
- Always use `RETURNING` clause for INSERT/UPDATE operations

```python
await cur.execute("""
    INSERT INTO categories (name, description)
    VALUES (%s, %s)
    RETURNING id, name, description
""", (category.name, category.description))
```

### Environment Variables

- Load from `.env` file using python-dotenv
- Define in `config.py`, expose via `settings.py`
- Required variables: `DB_CONN`, `PORT`

## Database

PostgreSQL connection uses psycopg async connection pool:

```python
import psycopg_pool
pool = psycopg_pool.ConnectionPool(settings.database_url)
```

## Adding New Features

1. **New Model**: Create in `src/kasir_api/models/`
2. **New Repository**: Create in `src/kasir_api/repositories/`
3. **New Handler**: Create in `src/kasir_api/handlers/`
4. **New Endpoint**: Register in `src/kasir_api/app.py`
