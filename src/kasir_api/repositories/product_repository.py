from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

from kasir_api.models.product import Product
from kasir_api.models.category import Category
from kasir_api.errors import NotFoundError, ConflictError

class ProductRepository:
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    @staticmethod
    def _to_model(row: dict) -> Product:
        return Product(**row)

    @staticmethod
    def _to_model_with_category(row: dict) -> Product:
        return Product(
            id=row["id"],
            name=row["name"],
            price=row["price"],
            stock=row["stock"],
            category_id=row["category_id"],
            category=Category(
                id=row["category_id"],
                name=row["category_name"],
                description=row["category_description"]
            )
        )

    async def get_all(self) -> list[Product]:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    SELECT p.id, p.name, p.price, p.stock, p.category_id,
                           c.id AS category_id,
                           c.name AS category_name,
                           c.description AS category_description
                    FROM products p
                    JOIN categories c ON p.category_id = c.id
                """)
                rows = await cur.fetchall()

        return [self._to_model_with_category(r) for r in rows]
    
    async def get_by_id(self, id: int) -> Product:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    SELECT p.id, p.name, p.price, p.stock, p.category_id,
                           c.id AS category_id,
                           c.name AS category_name,
                           c.description AS category_description
                    FROM products p
                    JOIN categories c ON p.category_id = c.id
                    WHERE p.id = %s
                """, (id,))
                row = await cur.fetchone()

        if not row:
            raise NotFoundError(f"Product dengan id {id} tidak ditemukan")
        return self._to_model_with_category(row)
    
    async def create(self, product: Product) -> Product:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO products (name, price, stock, category_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, name, price, stock, category_id
                """, (product.name, product.price, product.stock, product.category_id))
                row = await cur.fetchone()

        if not row:
            raise ConflictError("Gagal membuat product")
        return self._to_model(row)
    
    async def update(self, product: Product) -> Product:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    UPDATE products
                    SET name = %s, price = %s, stock = %s, category_id = %s
                    WHERE id = %s
                    RETURNING id, name, price, stock, category_id
                """, (product.name, product.price, product.stock, product.category_id, product.id))
                row = await cur.fetchone()

        if not row:
            raise NotFoundError(f"Product dengan id {product.id} tidak ditemukan")
        return self._to_model(row)
    
    async def delete(self, id: int) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    DELETE FROM products
                    WHERE id = %s
                """, (id,))

        if cur.rowcount == 0:
            raise NotFoundError(f"Product dengan id {id} tidak ditemukan")
