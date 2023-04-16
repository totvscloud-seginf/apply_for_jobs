
from app.domain.repositories.password_repository import PasswordRepository
from app.domain.exceptions.password_not_found_error import PasswordNotFoundError
from app.domain.entities.password import Password

class RetrievePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository) -> None:
        self.password_repository = password_repository

    def execute(self, url: str) -> Password:
        password = self.password_repository.get_password_by_url(url)
        if password is None:
            raise PasswordNotFound
        return password