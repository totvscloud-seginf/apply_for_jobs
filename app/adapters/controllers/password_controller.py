from domain.entities.password import Password
from domain.use_cases.generate_password_use_case import GeneratePasswordUseCase

class PasswordController:
    def __init__(self, password_use_case: GeneratePasswordUseCase) -> None:
        self.password_use_case = password_use_case

    def generate_password(self, password: Password) -> Password:
        return self.password_use_case.execute(password)

    def get_password(self, password: Password) -> Password:
        return self.password_use_case.get_password(password)

    def get_password_url(self, password: Password) -> str:
        return self.password_use_case.get_password_url(password)
    
    def get_password_by_url(self, url: str) -> Password:
        return self.password_use_case.get_password_by_url(url)
    
    def delete_password(self, password: Password) -> None:
        return self.password_use_case.delete_password(password)
    
