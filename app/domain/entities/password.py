import os
from datetime import datetime

from cryptography.fernet import Fernet
##import Crypto.Cipher.AES as crypto
import app.domain.exceptions.expired_password_error as expired_password_error
import app.domain.exceptions.invalid_visualizations_limit_error as invalid_visualizations_limit_error

class Password:
    def __init__(self, password: str, visualizations_limit: int, valid_until: datetime) -> None:
        self.password = self.cryptography(password, os.environ.get("PASS_CRYPTO_KEY") )
        self.visualizations_limit = visualizations_limit
        self.valid_until = valid_until
        self.views_count = 0
        self.url = f'abc/{password}'


    def view_password(self) -> str:
        if self.views_count >= self.visualizations_limit:
            raise invalid_visualizations_limit_error.InvalidVisualizationsLimitError
        if self.valid_until < datetime.now():
            raise expired_password_error.ExpiredPasswordError

        self.views_count += 1
        return self.password
    
    @staticmethod
    def cryptography(password: str, key: str) -> str:
        f = Fernet(bytes(key, encoding='utf8'))
        password: bytes = f.encrypt(password.encode())
        return password.decode()


    def is_valid(self) -> bool:
        return self.valid_until >= datetime.now() and self.views_count < self.visualizations_limit
    
    def __eq__(self, other):
        return self.password == other.password and self.visualizations_limit == other.visualizations_limit and self.valid_until == other.valid_until and self.views_count == other.views_count