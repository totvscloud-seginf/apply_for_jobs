from abc import ABC, abstractmethod
from typing import Optional

from ..entities.password import Password


class PasswordRepository(ABC):
    @abstractmethod
    def save_password(self, password: Password) -> None:
        pass

    @abstractmethod
    def get_password_by_url(self, url: str) -> Optional[Password]:
        pass

    @abstractmethod
    def get_password(self, password: str) -> Optional[Password]:
        pass

    @abstractmethod
    def delete_password(self, password: Password) -> None:
        pass
