'''
This file contains unit tests for the AdvancedErrorHandler class.
'''
import unittest
from unittest.mock import patch

from advanced_error_handler import AdvancedErrorHandler


class TestAdvancedErrorHandler(unittest.TestCase):
    def setUp(self):
        self.error_handler = AdvancedErrorHandler()

    def test_log_error(self):
        # Test logging an error with INFO severity
        with patch('logging.Logger.info') as mock_info:
            self.error_handler.log_error(Exception('Test error'), severity='INFO')
            mock_info.assert_called_once()
        # Test logging an error with WARNING severity
        with patch('logging.Logger.warning') as mock_warning:
            self.error_handler.log_error(Exception('Test error'), severity='WARNING')
            mock_warning.assert_called_once()
        # Test logging an error with ERROR severity
        with patch('logging.Logger.error') as mock_error:
            self.error_handler.log_error(Exception('Test error'), severity='ERROR')
            mock_error.assert_called_once()
        # Test logging an error with CRITICAL severity
        with patch('logging.Logger.critical') as mock_critical:
            self.error_handler.log_error(Exception('Test error'), severity='CRITICAL')
            mock_critical.assert_called_once()
        # Test logging an error with invalid severity
        with self.assertRaises(ValueError):
            self.error_handler.log_error(Exception('Test error'), severity='INVALID')

    def test_send_notification(self):
        # Test sending a notification without Slack API token and channel
        with patch('requests.post') as mock_post:
            self.error_handler.send_notification(Exception('Test error'))
            mock_post.assert_not_called()
        # Test sending a notification with Slack API token and channel
        self.error_handler.slack_api_token = 'TEST_API_TOKEN'
        self.error_handler.slack_channel = 'TEST_CHANNEL'
        with patch('requests.post') as mock_post:
            self.error_handler.send_notification(Exception('Test error'))
            mock_post.assert_called_once()

    def test_recover_from_error(self):
        # Test recovering from a non-critical error
        with patch('builtins.print') as mock_print:
            self.error_handler.recover_from_error(Exception('Test error'))
            mock_print.assert_called_once()

    def test_debug_info(self):
        # Test debugging information
        with patch('builtins.print') as mock_print:
            self.error_handler.debug_info(Exception('Test error'))
            mock_print.assert_called_once()

    def test_get_error_location(self):
        # Test getting the error location
        location = self.error_handler.get_error_location()
        self.assertIsInstance(location, str)

    def test_is_critical(self):
        # Test checking if an error is critical
        self.assertTrue(self.error_handler.is_critical(Exception('Test error')))

    def test_is_non_critical(self):
        # Test checking if an error is non-critical
        self.assertTrue(self.error_handler.is_non_critical(Exception('Test error')))

    def test_format_notification_message(self):
        # Test formatting a notification message
        message = self.error_handler.format_notification_message(Exception('Test error'))
        self.assertIsInstance(message, str)


if __name__ == '__main__':
    unittest.main()
