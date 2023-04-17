import app.domain.entities.password as entities
import app.domain.use_cases.password_use_case as use_cases

class PasswordController:
    """
    The controller for the password use case.
    """
    def __init__(self, password_use_case: use_cases.PasswordUseCase) -> None:
        self.password_use_case = password_use_case

    def set_password(self, password: entities.Password) -> entities.Password:
        """
        Sets the password for the given user.

        :param password: The password to set.
        :return: The password.
        """
        return self.password_use_case.execute(password)
    
    def get_password_by_id(self, id: str) -> entities.Password:        
        """
        Gets the password for the given pass id.

        :param id: The pass id.
        :return: The password.
        """
        return self.password_use_case.get_password_by_id(id)
    
    def delete_password(self, password: entities.Password) -> None:
        """
        Deletes the password for the given password

        :param password: The password to delete.
        """
        return self.password_use_case.delete_password(password)
    
