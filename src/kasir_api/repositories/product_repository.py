from kasir_api.models.product import Product
from kasir_api.repositories.db import pool

class ProductRepository:
    async def find_all(self) -> list[Product]:
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT id, name, price, stock, categoryid
                    FROM products
                """)
                rows = await cur.fetchall()

        return [Product(id=r[0], name=r[1], price=r[2], stock=r[3], categoryid=r[4]) for r in rows]
