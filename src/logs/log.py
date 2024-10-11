from datetime import datetime

class Logger:
    def __init__(self, log_file="/home/starias/africa_news_api/src/logs/app_log.txt", level='INFO'):
        """
        Initialize the logger with a log file and log level.
        
        Parameters:
        log_file (str): The file to write logs to.
        level (str): The default logging level (e.g., 'INFO', 'ERROR', 'DEBUG').
        """
        self.log_file = log_file
        self.level = level
        self.file = open(self.log_file, 'w', encoding='utf-8')  # Open file during initialization
        self.levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    def _get_timestamp(self):
        """
        Private method to generate a timestamp for each log entry.
        """
        timestamp_format = '%Y-%b-%d %H:%M:%S'  # Year-Monthname-Day Hour:Minute:Second
        current_time = datetime.now()
        return current_time.strftime(timestamp_format)

    def _log(self, message, level):
        """
        Private method to handle the actual logging.
        
        Parameters:
        message (str): The log message.
        level (str): The log level (e.g., 'INFO', 'ERROR').
        """
        if level not in self.levels:
            raise ValueError(f"Invalid log level: {level}. Must be one of {self.levels}")
        
        log_message = f"[{self._get_timestamp()}] [{level}] {message}\n"
        
        self.file.write(log_message)  # Write log message to file
        self.file.flush()  # Ensure the log message is written immediately

    def info(self, message):
        """Log an info message."""
        self._log(message, 'INFO')

    def error(self, message):
        """Log an error message."""
        self._log(message, 'ERROR')

    def debug(self, message):
        """Log a debug message."""
        self._log(message, 'DEBUG')

    def warning(self, message):
        """Log a warning message."""
        self._log(message, 'WARNING')

    def critical(self, message):
        """Log a critical message."""
        self._log(message, 'CRITICAL')

    def __del__(self):
        """
        Destructor to ensure the log file is properly closed when the Logger object is destroyed.
        """
        if self.file:
            self.file.close()

"""# Example usage
logger = Logger(log_file='app_log.txt')

logger.info('This is an info message.')
logger.error('An error occurred!')
logger.debug('Debugging information.')
logger.warning('This is a warning.')
logger.critical('Critical system failure!')
"""