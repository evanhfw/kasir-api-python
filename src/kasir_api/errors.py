class AppError(Exception):
    """Base class semua error di aplikasi."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    """Resource tidak ditemukan (404)."""
    pass


class ConflictError(AppError):
    """Data conflict / unique constraint (409)."""
    pass


class ValidationError(AppError):
    """Data tidak valid (400)."""
    pass


class UnauthorizedError(AppError):
    """Tidak punya akses (401)."""
    pass
