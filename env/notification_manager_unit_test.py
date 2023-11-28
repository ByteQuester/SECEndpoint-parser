'''
This module provides unit tests for the NotificationManager class.
'''
import unittest
from unittest.mock import MagicMock, patch

from notification_manager import NotificationManager
from logging_manager import LoggingManager


class TestNotificationManager(unittest.TestCase):
    def setUp(self):
        self.logging_manager = MagicMock()
        self.notification_manager = NotificationManager(self.logging_manager)

    def test_send_notification(self):
        message = 'This is a notification'
        with patch('notification_manager.LoggingManager.get_error_location') as mock_location:
            mock_location.return_value = 'test_location.py - test_function() - Line 123'
            self.notification_manager.send_notification(message)
            self.logging_manager.log.assert_called_with(f'Sent notification: {message}', 'INFO')

    def test_handle_error(self):
        error_message = 'An error occurred'
        with patch('notification_manager.LoggingManager.is_critical') as mock_critical:
            mock_critical.return_value = False
            self.notification_manager.handle_error(error_message)
            self.logging_manager.log.assert_called_with(f'Error: {error_message}', 'ERROR')


if __name__ == '__main__':
    unittest.main()
