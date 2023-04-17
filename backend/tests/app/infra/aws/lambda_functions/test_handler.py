import os
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from app.domain.entities.password import Password
from app.domain.use_cases.password_use_case import PasswordUseCase
from app.adapters.controllers.password_controller import PasswordController
from app.domain.exceptions.invalid_password_error import InvalidPasswordError
from app.domain.exceptions.password_not_found_error import PasswordNotFoundError
from ....base_tests import BaseTest

class LambdaHandlerTest(BaseTest):

    def setUp(self):
        self.password_repository_mock = MagicMock()
        self.use_case = PasswordUseCase(self.password_repository_mock)
        self.controller = PasswordController(self.use_case)

    def test_set_password_success(self):
        # Arrange
        body = {
            "password": "123456",
            "view_limit": 5,
            "valid_until": "7"
        }
        password = Password(
            password=body['password'],
            visualizations_limit=body['view_limit'],
            valid_until=datetime.timestamp(datetime.now()) + (int(body['valid_until']) * 86400) if body['valid_until'] else None,
        )
        self.password_repository_mock.create_password.return_value = password

        # Act
        response = self.controller.set_password(password)

        # Assert
        self.assertIsInstance(response, Password)
        self.assertEqual(response.password, password.password)
        self.assertEqual(response.visualizations_limit, password.visualizations_limit)
        self.assertEqual(response.valid_until, password.valid_until)

    def test_set_password_invalid_password(self):
        # Arrange
        body = {
            "password": "",
            "view_limit": 5,
            "valid_until": 7
        }

        password = Password(
            password=body['password'],
            visualizations_limit=body['view_limit'],
            valid_until=datetime.timestamp(datetime.now()) + (int(body['valid_until']) * 86400) if body['valid_until'] else None,
        )

        # Assert
        with self.assertRaises(InvalidPasswordError):
            self.controller.set_password(password)


    def test_get_password_by_id_success(self):
        # Arrange
        password_id = "some_id"
        password = Password(
            password=self.use_case.cryptography("123456", os.environ.get('PASS_CRYPTO_KEY')),
            visualizations_limit=5,
            views_count=3,
            valid_until=datetime.timestamp(datetime.now() + timedelta(days=7))
        )
        self.password_repository_mock.get_password_by_id.return_value = password

        # Act
        response = self.controller.get_password_by_id(password_id)

        # Assert
        self.assertIsInstance(response, Password)
        self.assertEqual(response.password, password.password)
        self.assertEqual(response.visualizations_limit, password.visualizations_limit)
        self.assertEqual(response.valid_until, password.valid_until)

    def test_get_password_by_id_password_not_found(self):
        # Arrange
        password_id = "some_id"
        self.password_repository_mock.get_password_by_id.return_value = None

        # Act
        with self.assertRaises(Exception):
            self.controller.get_password_by_id(password_id)
