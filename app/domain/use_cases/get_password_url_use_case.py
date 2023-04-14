from app.domain.repositories.password_repository import PasswordRepository

class GetPasswordUrlUseCase:
    def __init__(self, password_repository: PasswordRepository) -> None:
        self.password_repository = password_repository

    def execute(self, password: Password) -> str:
        url = self.password_repository.get_url_by_password(password)
        return url