from app.domain.exceptions.base_error import BaseError

class InvalidVisualizationsLimitError(BaseError):
    """
    Exception raised when a password has an invalid visualizations limit.
    """
    def __init__(self, id: str = ''):
        super().__init__('Invalid visualizations limit', 400, {'id': id})