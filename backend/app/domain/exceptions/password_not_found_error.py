from app.domain.exceptions.base_error import BaseError

class PasswordNotFoundError(BaseError):
    """
    Exception raised when a password is not found.
    """
    def __init__(self, id: str = ''):
        super().__init__('Password not found', 404, {'id': id})
