import datetime, uuid, os
from unittest.mock import Mock
from app.domain.entities.password import Password
from app.domain.exceptions.invalid_visualizations_limit_error import InvalidVisualizationsLimitError
from app.domain.exceptions.password_not_found_error import PasswordNotFoundError
from app.domain.exceptions.expired_password_error import ExpiredPasswordError
from app.domain.exceptions.base_error import BaseError
from app.domain.use_cases.password_use_case import PasswordUseCase
from ...base_tests import BaseTest

class PasswordUseCaseTest(BaseTest):
    
    def setUp(self):
        self.password_repository_mock = Mock()
        self.use_case = PasswordUseCase(self.password_repository_mock)

    def test_execute_should_save_password(self):
        # Arrange
        password = Password(
            password='mysecretpassword', 
            visualizations_limit=10, 
            valid_until=datetime.datetime(2023, 1, 1).timestamp()
        )
        self.password_repository_mock.save_password.return_value = password
        
        # Act
        result = self.use_case.execute(password)
        
        # Assert
        self.assertEqual(result, password)
        self.password_repository_mock.save_password.assert_called_once_with(password)

    def test_execute_should_raise_invalid_visualizations_limit_error(self):
        # Arrange
        password = Password(
            password='mysecretpassword', 
            visualizations_limit=0, 
            valid_until=datetime.datetime(2023, 1, 1).timestamp()
        )
        
        # Act/Assert
        with self.assertRaises(InvalidVisualizationsLimitError):
            self.use_case.execute(password)

    def test_get_password_by_id_should_return_password(self):
        # Arrange
        password_id = str(uuid.uuid4())
        password = Password(
            password='mysecretpassword', 
            visualizations_limit=10, 
            valid_until=datetime.datetime.now().timestamp() + 1000
        )
        password.view_password()
        password.password = PasswordUseCase.cryptography(password.password, os.environ.get('PASS_CRYPTO_KEY'))
        self.password_repository_mock.get_password_by_id.return_value = password
        
        # Act
        result = self.use_case.get_password_by_id(password_id)
        
        # Assert
        self.assertEqual(result, password)
        self.password_repository_mock.get_password_by_id.assert_called_once_with(password_id)

    def test_get_password_by_id_should_raise_expired_password_error(self):
        # Arrange
        password_id = str(uuid.uuid4())
        password = Password(
            password='mysecretpassword', 
            visualizations_limit=10, 
            views_count=5,
            valid_until=datetime.datetime(2020, 1, 1).timestamp()
        )
        self.password_repository_mock.get_password_by_id.return_value = password
        
        # Act/Assert
        with self.assertRaises(PasswordNotFoundError):
            self.use_case.get_password_by_id(password_id)

    def test_delete_password(self):
        # Arrange
        password = Password(
            password='mysecretpassword', 
            visualizations_limit=10, 
            valid_until=datetime.datetime(2023, 1, 1).timestamp()
        )
        
        # Act
        self.use_case.delete_password(password)
        
        # Assert
        self.password_repository_mock.delete_password.assert_called_once_with(password)
