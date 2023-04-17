import logging

class BaseError(BaseException):
    def __init__(self, message: str, status_code: int, extra: dict = None, *args):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        super().__init__(message)
        self.message = message
        self.status_code = status_code
        logging.error(message, exc_info=True, stack_info=True, extra=extra)

    def to_dict(self) -> dict:
        return {"message": self.message}