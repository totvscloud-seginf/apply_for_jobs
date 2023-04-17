import uuid
from unittest.mock import Mock
import app.domain.entities.password as entities
import app.domain.use_cases.password_use_case as use_cases
from app.adapters.controllers.password_controller import PasswordController
from ...base_tests import BaseTest

class TestPasswordController(BaseTest):
    def setUp(self):
        self.mock_use_case = Mock(spec=use_cases.PasswordUseCase)
        self.controller = PasswordController(self.mock_use_case)

    def test_set_password(self):
        mock_password = Mock(spec=entities.Password)
        self.mock_use_case.execute.return_value = mock_password
        result = self.controller.set_password(mock_password)
        self.assertEqual(result, mock_password)
        self.mock_use_case.execute.assert_called_once_with(mock_password)

    def test_get_password_by_id(self):
        url = uuid.uuid4()
        mock_password = Mock(spec=entities.Password)
        self.mock_use_case.get_password_by_id.return_value = mock_password
        result = self.controller.get_password_by_id(url)
        self.assertEqual(result, mock_password)
        self.mock_use_case.get_password_by_id.assert_called_once_with(url)

    def test_delete_password(self):
        mock_password = Mock(spec=entities.Password)
        self.controller.delete_password(mock_password)
        self.mock_use_case.delete_password.assert_called_once_with(mock_password)