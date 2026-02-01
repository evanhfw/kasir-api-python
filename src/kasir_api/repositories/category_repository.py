from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

from kasir_api.errors import NotFoundError, ConflictError
from kasir_api.models.category import Category

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
    
    async def get_by_id(self, id: int) -> Category:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    SELECT id, name, description
                    FROM categories
                    WHERE id = %s
                """, (id,))
                row = await cur.fetchone()

        if not row:
            raise NotFoundError(f"Category dengan id {id} tidak ditemukan")
        return self._to_model(row)
    
    async def create(self, category: Category) -> Category:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO categories (name, description)
                    VALUES (%s, %s)
                    RETURNING id, name, description
                """, (category.name, category.description))
                row = await cur.fetchone()

        if not row:
            raise ConflictError("Gagal membuat category")
        return self._to_model(row)
    
    
    async def update(self, category: Category) -> Category:
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    UPDATE categories
                    SET name = %s, description = %s
                    WHERE id = %s
                    RETURNING id, name, description
                """, (category.name, category.description, category.id))
                row = await cur.fetchone()

        if not row:
            raise NotFoundError(f"Category dengan id {category.id} tidak ditemukan")
        return self._to_model(row)
    
    async def delete(self, id: int) -> None:
        async with self.pool.connection() as conn:
            async with conn.transaction():
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute("""
                        DELETE FROM categories
                        WHERE id = %s
                    """, (id,))
                    if cur.rowcount == 0:
                        raise NotFoundError(f"Category dengan id {id} tidak ditemukan")