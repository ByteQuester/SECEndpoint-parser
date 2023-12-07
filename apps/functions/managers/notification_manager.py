'''
This module provides a NotificationManager class for sending notifications through the Command Line Interface (CLI) and logging all notification activities.
The NotificationManager class integrates the functionalities of the LoggingManager class for logging activities.
Example usage:
    # Create an instance of NotificationManager
    notification_manager = NotificationManager(logging_manager)
    # Send a CLI notification
    notification_manager.send_notification('This is a notification')
    # Validate notification content
    is_valid = notification_manager.validate_notification_content('Notification content')
    # Handle an error
    notification_manager.handle_error('An error occurred')
'''

from apps.functions.managers import LoggingManager


class NotificationManager:
    def __init__(self, logging_manager):
        self.logging_manager = logging_manager

    def send_notification(self, message):
        '''
        Send a CLI notification.
        Parameters:
            message (str): The notification message.
        '''
        try:
            # Simulate sending a notification (just a print statement here)
            print(message)
            self.logging_manager.log(f'Sent notification: {message}', 'INFO')
        except Exception as e:
            error_location = LoggingManager.get_error_location()
            self.handle_error(f'Error sending notification: {str(e)} at {error_location}')

    def handle_error(self, error_message):
        '''
        Handle an error during notification processes.
        Parameters:
            error_message (str): The error message.
        '''
        print(f'Error: {error_message}')
        critical = LoggingManager.is_critical(Exception(error_message))
        severity = 'CRITICAL' if critical else 'ERROR'
        self.logging_manager.log(f'Error: {error_message}', severity)