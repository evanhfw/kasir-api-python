from kasir_api.config import DATABASE_URL, PORT

class Settings:
    database_url: str = DATABASE_URL
    port: int = PORT

settings = Settings()