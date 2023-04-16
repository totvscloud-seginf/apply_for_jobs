import datetime
from unittest.mock import Mock
from app.domain.entities.password import Password
from app.domain.exceptions.invalid_visualizations_limit_error import InvalidVisualizationsLimitError
from app.domain.exceptions.password_not_found_error import PasswordNotFoundError
from app.domain.use_cases.generate_password_use_case import GeneratePasswordUseCase
from ...base_tests import BaseTest

class GeneratePasswordUseCaseTest(BaseTest):
    
    def setUp(self):
        self.password_repository_mock = Mock()
        self.use_case = GeneratePasswordUseCase(self.password_repository_mock)

    def test_execute_should_save_password(self):
        # Arrange
        password = Password(password='mysecretpassword', visualizations_limit=10, valid_until=datetime.datetime(2023, 1, 1))
        self.password_repository_mock.save_password.return_value = password
        
        # Act
        result = self.use_case.execute(password)
        
        # Assert
        self.assertEqual(result, password)
        self.password_repository_mock.save_password.assert_called_once_with(password)

    def test_execute_should_raise_invalid_visualizations_limit_error(self):
        # Arrange
        password = Password(password='mysecretpassword', visualizations_limit=0, valid_until=datetime.datetime(2023, 1, 1))
        
        # Act/Assert
        with self.assertRaises(InvalidVisualizationsLimitError):
            self.use_case.execute(password)
    
    def test_generate_random_password_should_return_string_with_given_length(self):
        # Arrange
        length = 10
        characters = 'abcdef'
        
        # Act
        password = self.use_case.generate_random_password(length, characters)
        
        # Assert
        self.assertEqual(len(password), length)

    def test_get_password_url_should_return_url(self):
        # Arrange
        password = Password(password='mysecretpassword', visualizations_limit=10, valid_until=datetime.datetime(2023, 1, 1))
        self.password_repository_mock.get_url_by_password.return_value = 'http://password.com'
        
        # Act
        result = self.use_case.get_password_url(password)
        
        # Assert
        self.assertEqual(result, 'http://password.com')
        self.password_repository_mock.get_url_by_password.assert_called_once_with(password)

    def test_get_password_by_url_should_return_password(self):
        # Arrange
        url = 'http://password.com'
        password = Password(password='mysecretpassword', visualizations_limit=10, valid_until=datetime.datetime(2023, 1, 1))
        self.password_repository_mock.get_password_by_url.return_value = password
        
        # Act
        result = self.use_case.get_password_by_url(url)
        
        # Assert
        self.assertEqual(result, password)
        self.password_repository_mock.get_password_by_url.assert_called_once_with(url)

    def test_retrieve_password_should_raise_password_not_found_error(self):
        # Arrange
        url = 'http://password.com'
        self.password_repository_mock.get_password_by_url.return_value = None
        
        # Act/Assert
        with self.assertRaises(PasswordNotFoundError):
            self.use_case.retrieve_password(url)

    def test_validate_password_should_return_true(self):
        # Arrange
        password = 'mysecretpassword'
        self.password_repository_mock.validate_password.return_value = True
        
        # Act
        result = self.use_case.validate_password(password)
        
        # Assert
        self.assertTrue(result)
        self.password_repository_mock.validate_password.assert_called_once_with(password)