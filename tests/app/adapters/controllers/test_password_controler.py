import unittest
from unittest.mock import Mock
import app.domain.entities.password as entities
import app.domain.use_cases.generate_password_use_case as use_cases
from app.adapters.controllers.password_controller import PasswordController
from ...base_tests import BaseTest

class TestPasswordController(BaseTest):
    def setUp(self):
        self.mock_use_case = Mock(spec=use_cases.GeneratePasswordUseCase)
        self.controller = PasswordController(self.mock_use_case)

    def test_generate_password(self):
        mock_password = Mock(spec=entities.Password)
        self.mock_use_case.execute.return_value = mock_password
        result = self.controller.generate_password(mock_password)
        self.assertEqual(result, mock_password)
        self.mock_use_case.execute.assert_called_once_with(mock_password)

    def test_get_password_url(self):
        mock_password = Mock(spec=entities.Password)
        self.mock_use_case.get_password_url.return_value = 'https://example.com'
        result = self.controller.get_password_url(mock_password)
        self.assertEqual(result, 'https://example.com')
        self.mock_use_case.get_password_url.assert_called_once_with(mock_password)

    def test_get_password_by_url(self):
        url = 'https://example.com'
        mock_password = Mock(spec=entities.Password)
        self.mock_use_case.get_password_by_url.return_value = mock_password
        result = self.controller.get_password_by_url(url)
        self.assertEqual(result, mock_password)
        self.mock_use_case.get_password_by_url.assert_called_once_with(url)

    def test_delete_password(self):
        mock_password = Mock(spec=entities.Password)
        self.controller.delete_password(mock_password)
        self.mock_use_case.delete_password.assert_called_once_with(mock_password)