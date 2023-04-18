import os
from cryptography.fernet import Fernet

from ..repositories.password_repository import PasswordRepository
from ..exceptions.invalid_visualizations_limit_error import InvalidVisualizationsLimitError
from ..exceptions.invalid_password_error import InvalidPasswordError
from ..exceptions.password_not_found_error import PasswordNotFoundError
from ..exceptions.expired_password_error import ExpiredPasswordError
from ..entities.password import Password

class PasswordUseCase:
    def __init__(self, password_repository: PasswordRepository) -> None:
        self.password_repository = password_repository

    def execute(self, password: Password) -> Password:
        if not self.validate_password(password):
            raise InvalidPasswordError(password.id)
        
        if password.visualizations_limit <= 0:
            raise InvalidVisualizationsLimitError(password.id)

        password.password = self.cryptography(password.password, os.environ.get('PASS_CRYPTO_KEY'))
        self.password_repository.save_password(password)
        return password
    
    def get_password_by_id(self, id: str) -> Password:
        # try to get password
        try :
            # get password from repo
            password = self.password_repository.get_password_by_id(id)
            password.view_password()
            password.password = self.decryptography(password.password, os.environ.get('PASS_CRYPTO_KEY'))
        except (InvalidVisualizationsLimitError, ExpiredPasswordError) as e:
            # if error, delete password and raise exception
            self.delete_password(password)
            raise PasswordNotFoundError(id)

        return password

    def retrieve_password(self, id: str) -> Password:
        password = self.password_repository.get_password_by_id(id)
        if password is None:
            raise PasswordNotFoundError(id)
        return password

    @staticmethod
    def cryptography(password: str, key: str) -> str:
        f = Fernet(bytes(key, encoding='utf8'))
        password: bytes = f.encrypt(password.encode())
        return password.decode()
    
    @staticmethod
    def decryptography(password: str, key: str) -> str:
        f = Fernet(bytes(key, encoding='utf8'))
        password: bytes = f.decrypt(password.encode())
        return password.decode()

    def delete_password(self, password: Password) -> None:
        self.password_repository.delete_password(password)

    def validate_password(self, password: Password) -> bool:
        if password.password is None or password.password == '':
            return False
         
        return True
