from abc import ABC, abstractmethod
from typing import Optional

import app.domain.entities.password as entities


class PasswordRepository(ABC):
    @abstractmethod
    def save_password(self, password: entities.Password) -> None:
        pass

    @abstractmethod
    def get_password_by_url(self, url: str) -> Optional[entities.Password]:
        pass

    @abstractmethod
    def get_password(self, password: str) -> Optional[entities.Password]:
        pass

    @abstractmethod
    def delete_password(self, password: entities.Password) -> None:
        pass
