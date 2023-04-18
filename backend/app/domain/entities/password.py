import uuid
from datetime import datetime
from typing import TypedDict, Optional
from typing_extensions import Unpack

import app.domain.exceptions.expired_password_error as expired_password_error
import app.domain.exceptions.invalid_visualizations_limit_error as invalid_visualizations_limit_error

class PassArgs(TypedDict):
    password: str
    visualizations_limit: int
    valid_until: float
    views_count: int
    id: str

class Password:
    """Class that represents a password
    """
    def __init__( self, **kwargs: Unpack[PassArgs] ) -> None:
        """Constructor of the class.
        
        Args:
            password (str): The password to store.
            visualizations_limit (int): The number of times the password can be viewed.
            valid_until (float, optional): The timestamp of the password's expiration. If it is None, the password never expires. Defaults to None.
        """
        self.password = kwargs.get('password')
        self.visualizations_limit = kwargs.get('visualizations_limit')
        self.valid_until = kwargs.get('valid_until')
        self.views_count = kwargs.get('views_count')
        self.id = kwargs.get('id') if kwargs.get('id') else str(uuid.uuid4())

    def view_password(self) -> str:
        """Returns the password if it's valid and raises an exception otherwise.
        Raises:
            invalid_visualizations_limit_error.InvalidVisualizationsLimitError: If the number of visualizations is greater than the limit.
            expired_password_error.ExpiredPasswordError: If the password has expired.
        Returns:
            str: The password.
        """
        if self.views_count >= self.visualizations_limit:
            raise invalid_visualizations_limit_error.InvalidVisualizationsLimitError(self.id)
        
        if self.valid_until is not None and self.valid_until < datetime.now().timestamp():
            raise expired_password_error.ExpiredPasswordError(self.id)

        self.views_count += 1
        return self.password        