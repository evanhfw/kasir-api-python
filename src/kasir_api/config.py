import os

from dotenv import load_dotenv

load_dotenv()

_db_conn = os.getenv("DB_CONN")
if _db_conn is None:
    raise RuntimeError("Environment variable DB_CONN is required")

DATABASE_URL: str = _db_conn
PORT = int(os.getenv("PORT", 8000))