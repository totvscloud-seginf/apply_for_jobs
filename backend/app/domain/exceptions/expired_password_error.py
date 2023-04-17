from app.domain.exceptions.base_error import BaseError

class ExpiredPasswordError(BaseError):
    """
    Exception raised when a password is expired.
    """
    def __init__(self, id: str = ''):
        super().__init__('Password expired', 400, {'id': id})
