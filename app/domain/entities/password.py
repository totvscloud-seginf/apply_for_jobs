import os
from datetime import datetime
from cryptography.fernet import Fernet

from ..exceptions.expired_password_error import ExpiredPasswordError
from ..exceptions.invalid_visualizations_limit_error import InvalidVisualizationsLimitError

class Password:
    def __init__(self, password: str, visualizations_limit: int, valid_until: datetime) -> None:
        self.password = self.cryptography(password, os.environ.get("PASS_CRYPTO_KEY") )
        self.visualizations_limit = visualizations_limit
        self.valid_until = valid_until
        self.views_count = 0
        self.url = f'123456/{password}'


    def view_password(self) -> str:
        if self.views_count >= self.visualizations_limit:
            raise InvalidVisualizationsLimitError
        if self.valid_until < datetime.now():
            raise ExpiredPasswordError

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