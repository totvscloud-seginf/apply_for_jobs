from abc import ABC, abstractmethod
from typing import Optional

import app.domain.entities.password as entities


class PasswordRepository(ABC):
    @abstractmethod
    def save_password(self, password: entities.Password) -> None:
        """Save a new password to the repository."""
        pass

    @abstractmethod
    def get_password_by_id(self, id: str) -> Optional[entities.Password]:
        """Return the password with the given ID."""
        pass

    @abstractmethod
    def delete_password(self, password: entities.Password) -> None:
        """Delete the password from the repository."""
        pass
