'''
This file contains the implementation of the AdvancedErrorHandler class.
'''

import logging
import datetime
import traceback
import os
import requests
import time


class AdvancedErrorHandler:
    def __init__(self, log_file_path='error_log.txt', notification_threshold='ERROR', slack_api_token=None,
                 slack_channel=None):
        '''
        Initialize the AdvancedErrorHandler class.
        Parameters:
        - log_file_path (str): Path to the log file.
        - notification_threshold (str): Severity level threshold for notifications.
        - slack_api_token (str): API token for Slack integration.
        - slack_channel (str): Slack channel to post notifications.
        '''
        self.log_file_path = log_file_path
        self.notification_threshold = notification_threshold
        self.slack_api_token = slack_api_token
        self.slack_channel = slack_channel
        # Configure logging
        logging.basicConfig(filename=self.log_file_path, level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def log_error(self, error, severity='INFO'):
        '''
        Log the error with detailed information.
        Parameters:
        - error (Exception): The error to be logged.
        - severity (str): Severity level of the error (INFO, WARNING, ERROR, CRITICAL).
        '''
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        location = self.get_error_location()
        message = f'{error.__class__.__name__}: {str(error)}'
        log_message = f'{timestamp} - {severity} - {location} - {message}'
        # Get the logger object with a unique name for the AdvancedErrorHandler class
        logger = logging.getLogger('AdvancedErrorHandler')
        # Log the error with the appropriate severity level
        if severity == 'INFO':
            logger.info(log_message)
        elif severity == 'WARNING':
            logger.warning(log_message)
        elif severity == 'ERROR':
            logger.error(log_message)
        elif severity == 'CRITICAL':
            logger.critical(log_message)
        else:
            raise ValueError(f'Invalid severity level: {severity}')

    def send_notification(self, error, severity=None):
        '''
        Send notifications/alerts when critical errors occur.
        Parameters:
        - error (Exception): The critical error that occurred.
        - severity (str): Severity level of the error (INFO, WARNING, ERROR, CRITICAL).
                          If not provided, the default severity level specified during initialization will be used.
        '''
        if severity is None:
            severity = self.notification_threshold
        if self.is_critical(error):
            notification_message = self.format_notification_message(error)
            try:
                if self.slack_api_token and self.slack_channel:
                    headers = {
                        'Authorization': f'Bearer {self.slack_api_token}',
                        'Content-Type': 'application/json'
                    }
                    payload = {
                        'channel': self.slack_channel,
                        'text': notification_message
                    }
                    response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, json=payload)
                    response.raise_for_status()  # Raise an exception for non-2xx status codes
                    print(f'Successfully sent notification: {notification_message}')
                else:
                    print(f'Sending notification: {notification_message}')
            except (requests.RequestException, Exception) as e:
                self.log_error(e, severity='ERROR')
                print(f'Failed to send notification: {str(e)}')

    def recover_from_error(self, error):
        '''
        Attempt to recover from non-critical errors.
        Parameters:
        - error (Exception): The non-critical error that occurred.
        '''
        if self.is_non_critical(error):
            recovery_message = f'Recovering from error: {error}'
            # Implement the code for recovery here
            if isinstance(error, ConnectionError):
                # Retry the failed operation
                self.retry_operation()
            elif isinstance(error, TimeoutError):
                # Switch to a fallback process
                self.switch_to_fallback()
            elif isinstance(error, ValueError):
                # Reset components to a safe state
                self.reset_components()
            else:
                # Handle other types of non-critical errors
                self.handle_other_errors()
            # Log the recovery process
            self.log_error(recovery_message, severity='INFO')
            print(recovery_message)

    def retry_operation(self):
        '''
        Retry the failed operation.
        '''
        max_retries = 5
        retry_delay = 1  # seconds
        for attempt in range(max_retries):
            try:
                # Implement the retry logic here
                print(f'Retrying operation... Attempt {attempt+1}')
                # Simulating a failed operation
                raise ConnectionError('Connection failed')
            except ConnectionError as e:
                self.log_error(e, severity='ERROR')
                print(f'Failed to retry operation: {str(e)}')
                time.sleep(retry_delay * 2**attempt)
            else:
                print('Operation successful')
                break
        else:
            print('Max retries exceeded')

    def switch_to_fallback(self):
        '''
        Switch to a fallback process.
        '''
        # Implement the fallback logic here
        self.log_error('Switching to fallback process', severity='INFO')
        print('Switching to fallback process')
        # Return a boolean indicating the success of the fallback process
        return True

    def reset_components(self):
        '''
        Reset components to a safe state.
        '''
        # Implement the reset logic here
        self.log_error('Resetting components to a safe state', severity='INFO')
        print('Resetting components to a safe state')

    def handle_other_errors(self):
        '''
        Handle other types of non-critical errors.
        '''
        # Implement the logic for handling other errors here
        self.log_error('Handling other non-critical errors', severity='INFO')
        print('Handling other non-critical errors')

    def debug_info(self, error):
        '''
        Gather and log relevant debugging information upon encountering an error.
        Parameters:
        - error (Exception): The error that occurred.
        '''
        traceback_message = traceback.format_exc()
        # Log the debugging information
        self.log_error(traceback_message, severity='DEBUG')
        # Print the debugging information
        print(f'Debugging information: {traceback_message}')

    def get_error_location(self):
        '''
        Get the location in the code where the error occurred.
        Returns:
        - str: The location in the code where the error occurred.
        '''
        traceback_info = traceback.extract_stack()[:-1]  # Exclude the current method from the traceback
        file_path, line_number, function_name, _ = traceback_info[-1]
        return f'{file_path} - {function_name}() - Line {line_number}'

    def is_critical(self, error):
        '''
        Check if the error is critical based on the severity level threshold.
        Parameters:
        - error (Exception): The error to be checked.
        Returns:
        - bool: True if the error is critical, False otherwise.
        '''
        return logging.getLogger().getEffectiveLevel() >= logging.getLevelName(self.notification_threshold)

    def is_non_critical(self, error):
        '''
        Check if the error is non-critical based on the severity level threshold.
        Parameters:
        - error (Exception): The error to be checked.
        Returns:
        - bool: True if the error is non-critical, False otherwise.
        '''
        return logging.getLogger().getEffectiveLevel() <= logging.getLevelName(self.notification_threshold)

    def format_notification_message(self, error):
        '''
        Format the notification message with detailed error information.
        Parameters:
        - error (Exception): The error to be included in the message.
        Returns:
        - str: The formatted notification message.
        '''
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        location = self.get_error_location()
        error_type = error.__class__.__name__
        error_message = str(error)
        return f'{timestamp} - Error Type: {error_type}\nLocation: {location}\nMessage: {error_message}'
