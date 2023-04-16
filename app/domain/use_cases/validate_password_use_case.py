from ..repositories.password_repository import PasswordRepository

class ValidatePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository = password_repository

    def execute(self, password: str) -> bool:
        return self.password_repository.validate_password(password)