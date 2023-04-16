import random
import datetime
from ..repositories.password_repository import PasswordRepository
from ..exceptions.invalid_visualizations_limit_error import InvalidVisualizationsLimitError
from ..exceptions.password_not_found_error import PasswordNotFoundError
from ..exceptions.expired_password_error import ExpiredPasswordError
from ..entities.password import Password

class GeneratePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository) -> None:
        self.password_repository = password_repository

    def execute(self, password: Password) -> Password:
        if password.visualizations_limit <= 0:
            raise InvalidVisualizationsLimitError

        self.password_repository.save_password(password)
        return password

    def generate_random_password(self, password_length: int, password_characters: str) -> str:
        password = ''.join(random.choice(password_characters) for i in range(password_length))
        return password

    def get_password_url(self, password: Password) -> str:
        url = self.password_repository.get_url_by_password(password)
        return url
    
    def get_password_by_url(self, url: str) -> Password:
        password = self.password_repository.get_password_by_url(url)
        return password

    def retrieve_password(self, url: str) -> Password:
        password = self.password_repository.get_password_by_url(url)
        if password is None:
            raise PasswordNotFoundError
        return password

    def validate_password(self, password: str) -> bool:
        return self.password_repository.validate_password(password)

    def view_password(self, password: Password) -> str:
        if password.views_count >= password.visualizations_limit:
            raise InvalidVisualizationsLimitError
        if password.valid_until < datetime.now():
            raise ExpiredPasswordError

        password.views_count += 1
        return password.password

    def is_password_valid(self, password: Password) -> bool:
        return password.valid_until >= datetime.now() and password.views_count < password.visualizations_limit
    
    def delete_password(self, password: Password) -> None:
        self.password_repository.delete_password(password)
