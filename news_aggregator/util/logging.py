# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Logging handler and logic.

Loggers manage multiple threads with no need for extra configuration:
    - https://docs.python.org/3/howto/logging-cookbook.html#logging-from-multiple-threads

And it can write to different destinations, even depending on the log level. This is not useful for this project though:
    - https://docs.python.org/3/howto/logging-cookbook.html#logging-to-multiple-destinations

Check this part of the cookbook if non-blocking log writing is needed:
    - https://docs.python.org/3/howto/logging-cookbook.html#dealing-with-handlers-that-block

TODO: Hacer que este logger trabaje sólo con JSON. ¿emit?.
"""
import logging
from logging import Logger, LogRecord
from logging.handlers import TimedRotatingFileHandler

from const.data import LOGGING_MIN_LEVEL, LOGGING_FILE_PATH, LOGGING_MESSAGE_FORMAT
from util.design_patterns import SingletonMetaclass


class AppLogFilter(logging.Filter):
    """Filter that prevents the writing of user's sensible data in the log files"""

    _record_fields_to_be_filtered = ["password", "passwd", "pwd"]

    def filter(self, record: LogRecord) -> bool:
        # The message will only be ignored by the filter if it does not contain any of the keywords contained in
        # self._record_fields_to_be_filtered.
        return not any(field in record.getMessage().lower() for field in self._record_fields_to_be_filtered)


class AppLogger(Logger, metaclass=SingletonMetaclass):
    """Custom logger class to be used over all the application, when needed"""

    def __init__(self, *args, **kwargs):
        """Creates and configures the logging handler"""
        super(AppLogger).__init__(*args, **kwargs)

        self._logger = logging.getLogger("AppLogger")

        self._logger.setLevel(LOGGING_MIN_LEVEL)

        # There will be only one handler.
        # https://docs.python.org/3/howto/logging.html#useful-handlers
        # Handler configuration:
        #   - The file in which the log messages will be written is specified in "LOGGING_FILE_PATH".
        #   - Each log file will be rotated by midnight ("when" kwarg). Note that the rollover is tied to the emission
        #   of log messages. This means that if no message is emitted for a period of 5 hours after midnight, the
        #   rollover won't be done until the first log message is emitted, 5 hours after midnight in this case.
        #   - The file opening will be deferred until the first log message is emitted ("delay" kwarg).
        #   - A maximum of 10 files will be held ("backupCount" kwarg). If a new file is created and there are 10 stored
        #   log files already, the oldest one will be deleted.
        #   - The files will be encoded using UTF-8.
        #   -
        timed_rotating_handler = TimedRotatingFileHandler(filename=LOGGING_FILE_PATH, when="midnight", backupCount=10,
                                                          delay=True, encoding="UTF-8")

        # Special format for the emitted messages.
        formatter = logging.Formatter(LOGGING_MESSAGE_FORMAT)
        timed_rotating_handler.setFormatter(formatter)

        # A filter must be set, to prevent the writing of user sensible information in the log files.
        self._logger.addFilter(AppLogFilter())

        # Finally, add the handler to the logger.
        self._logger.addHandler(timed_rotating_handler)

    @property
    def logger(self):
        """Getter for the properly configured internal logger object"""
        return self._logger
