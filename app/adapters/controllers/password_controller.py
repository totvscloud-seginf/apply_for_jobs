import app.domain.entities.password as entities
import app.domain.use_cases.generate_password_use_case as use_cases

class PasswordController:
    def __init__(self, password_use_case: use_cases.GeneratePasswordUseCase) -> None:
        self.password_use_case = password_use_case

    def generate_password(self, password: entities.Password) -> entities.Password:
        return self.password_use_case.execute(password)

    def get_password(self, password: entities.Password) -> entities.Password:
        return self.password_use_case.get_password(password)

    def get_password_url(self, password: entities.Password) -> str:
        return self.password_use_case.get_password_url(password)
    
    def get_password_by_url(self, url: str) -> entities.Password:
        return self.password_use_case.get_password_by_url(url)
    
    def delete_password(self, password: entities.Password) -> None:
        return self.password_use_case.delete_password(password)
    
