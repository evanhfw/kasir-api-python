# Kasir API Python

A Point of Sale (Kasir) REST API built with FastAPI and PostgreSQL.

## Tech Stack

- **Language**: Python 3.14+
- **Framework**: FastAPI
- **Database**: PostgreSQL via psycopg (async)
- **Validation**: Pydantic
- **Package Manager**: uv

## Features

- Health check endpoint
- Categories CRUD operations
- Products CRUD operations
- Async database operations
- Auto-generated API documentation

## Quick Start

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) package manager
- PostgreSQL database

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd kasir-api-python
   ```

2. Copy environment file and configure:

   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and set your database connection string:

   ```
   DB_CONN=postgresql://user:password@localhost:5432/kasir_db
   PORT=8000
   ```

4. Install dependencies:

   ```bash
   uv sync
   ```

5. Run the development server:

   ```bash
   uv run fastapi dev src/kasir_api/app.py
   ```

   For production:

   ```bash
   uv run fastapi run src/kasir_api/app.py --port 8000
   ```

## Environment Variables

| Variable | Required | Default | Description                     |
|----------|----------|---------|--------------------------------|
| DB_CONN  | Yes      | -       | PostgreSQL connection string   |
| PORT     | No       | 8000    | Server port                    |

## API Endpoints

| Method | Endpoint               | Description          |
|--------|------------------------|----------------------|
| GET    | /api/health            | Health check         |
| GET    | /api/categories        | Get all categories   |
| GET    | /api/categories/{id}   | Get category by ID   |
| POST   | /api/categories        | Create category      |
| PUT    | /api/categories/{id}   | Update category      |
| DELETE | /api/categories/{id}   | Delete category      |
| GET    | /api/products          | Get all products     |
| GET    | /api/products/{id}     | Get product by ID    |
| POST   | /api/products          | Create product       |
| PUT    | /api/products/{id}     | Update product       |
| DELETE | /api/products/{id}     | Delete product       |

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
src/kasir_api/
├── app.py                    # FastAPI application entry point
├── config.py                 # Environment variable loading
├── settings.py               # Settings class
├── errors.py                 # Custom exception classes
├── lifespan.py               # Application lifespan management
├── models/                   # Pydantic models
│   ├── category.py
│   ├── health.py
│   └── product.py
├── repositories/             # Database access layer
│   ├── db.py
│   ├── category_repository.py
│   ├── health_repository.py
│   └── product_repository.py
├── services/                 # Business logic layer
│   ├── category_service.py
│   ├── health_service.py
│   └── product_service.py
└── handlers/                 # Request handlers (routes)
    ├── category_handler.py
    ├── health_handler.py
    └── product_handler.py
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src/kasir_api
```
