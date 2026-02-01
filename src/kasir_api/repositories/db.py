from psycopg_pool import AsyncConnectionPool

from kasir_api.settings import settings

pool = AsyncConnectionPool(settings.database_url, open=False)
