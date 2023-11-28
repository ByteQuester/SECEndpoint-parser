'''
This module provides a LoggingManager class for managing logging activities.
The LoggingManager class allows setting up log file paths and logging messages with various severity levels.
Example usage:
    # Create an instance of LoggingManager
    logger = LoggingManager()
    # Set the log file path
    logger.set_log_file_path('path/to/logfile.log')
    # Set the log message format
    logger.set_log_format('%(asctime)s - %(levelname)s - %(message)s')
    # Log a message with severity level INFO
    logger.log('This is an informational message', 'INFO')
    # Log a message with severity level ERROR
    logger.log('An error occurred', 'ERROR')
'''

import logging
import datetime
import traceback


class LoggingManager:
    def __init__(self):
        self.log_file_path = None
        self.log_format = None
        self.log_level = logging.INFO
        self._configure_logging()

    def set_log_file_path(self, path):
        '''
        Set the log file path.
        Parameters:
            path (str): The path to the log file.
        '''
        self.log_file_path = path
        self._configure_logging()

    def set_log_format(self, format):
        '''
        Set the log message format.
        Parameters:
            format (str): The log message format.
        '''
        self.log_format = format
        self._configure_logging()

    def set_log_level(self, level):
        '''
        Set the logging level.
        Parameters:
            level (str): The logging level as a string.
        '''
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if level in valid_levels:
            self.log_level = getattr(logging, level)
            self._configure_logging()
        else:
            logging.warning(f'Invalid log level "{level}". Using default log level "INFO".')

    def _configure_logging(self):
        '''
        Configure the logging module based on the log file path, log format, and log level.
        '''
        if self.log_file_path:
            logging.basicConfig(filename=self.log_file_path, level=self.log_level, format=self.log_format)
        else:
            logging.basicConfig(level=self.log_level, format=self.log_format)

    def is_critical(self, error):
        """
        Check if the error is critical based on the severity level threshold.
        """
        error_severity = self.get_error_severity(error)
        return error_severity >= logging.ERROR

    @staticmethod
    def get_error_severity(error):
        '''
        Get the severity level of the error.
        '''
        severity_mapping = {
            ConnectionError: logging.CRITICAL,
            TimeoutError: logging.CRITICAL,
            ValueError: logging.WARNING,
            Exception: logging.ERROR
        }
        # Determine the error type and map it to the corresponding severity level
        for error_type, severity_level in severity_mapping.items():
            if isinstance(error, error_type):
                return severity_level
        # Default severity level if the error type is not in the mapping
        return logging.ERROR

    def log_error(self, error, severity='INFO'):
        '''
        Log the error with detailed information.
        Parameters:
        - error (Exception): The error to be logged.
        - severity (str): Severity level of the error (INFO, WARNING, ERROR, CRITICAL, DEBUG).
        '''
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        location = self.get_error_location()
        message = f'{error.__class__.__name__}: {str(error)}'
        log_message = f'{timestamp} - {severity} - {location} - {message}'
        # Get the logger object with a unique name for the AdvancedErrorHandler class
        logger = logging.getLogger('__name__')
        # Log the error with the appropriate severity level
        if severity == 'INFO':
            logger.info(log_message)
        elif severity == 'WARNING':
            logger.warning(log_message)
        elif severity == 'ERROR':
            logger.error(log_message)
        elif severity == 'CRITICAL':
            logger.critical(log_message)
        elif severity == 'DEBUG':
            logger.debug(log_message)
        else:
            raise ValueError(f'Invalid severity level: {severity}')

    @staticmethod
    def get_error_location():
        """
        Get the location in the code where the error occurred.
        Returns:
            str: The location in the code where the error occurred.
        """
        traceback_info = traceback.extract_stack()[:-2]  # Exclude the current method and caller from the traceback
        file_path, line_number, function_name, _ = traceback_info[-1]
        return f'{file_path} - {function_name}() - Line {line_number}'

    @staticmethod
    def format_log_message(message, message_type):
        """
        Format the log message with additional information.
        Parameters:
            message (str): The message to be formatted.
            message_type (str): The type of the message (e.g., 'INFO', 'ERROR').
        Returns:
            str: The formatted log message.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f"{timestamp} - {message_type} - {message}"
        return formatted_message

    @staticmethod
    def log(message, severity):
        '''
        Log a message with the specified severity level.
        Parameters:
            message (str): The message to be logged.
            severity (str): The severity level of the log message as a string.
        '''
        valid_severity_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if severity in valid_severity_levels:
            severity = getattr(logging, severity)
        else:
            logging.warning(f'Invalid severity level "{severity}". Using default severity level "INFO".')
            severity = logging.INFO
        logging.log(severity, message)