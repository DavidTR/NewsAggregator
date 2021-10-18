# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Const values.

"""
import logging
import os
import sys

# Parent directory of the current file, as we are inside the "const" package.
PROJECT_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# Since Python 3 is unbounded, which means that the maximum representable integer value is limited by the memory's word
# size, which is held as a constant value in the "sys" module. Signed values are supported.
# See: https://stackoverflow.com/a/7604981.
MAX_PYTHON_INT_VALUE = sys.maxsize
MIN_PYTHON_INT_VALUE = -sys.maxsize - 1

# These are the maximum and minimum integer supported values in MySQL. Expand with the required int-ish
# (SMALLINT, TINYINT, etc...) precision values. Since these are more "restricting" values than the unbounded Python
# precision ones, they will be considered the default precision constraints for ints. This will prevent database
# overflow errors when dealing with INT columns.
# See: https://dev.mysql.com/doc/refman/8.0/en/integer-types.html.
MAX_INT_VALUE = 2147483647
MIN_INT_VALUE = -2147483648

LOGGING_MESSAGES_PATTERN = ""
LOGGING_MIN_LEVEL = logging.DEBUG
LOGGING_FILE_PATH = os.path.join(PROJECT_ROOT_PATH, "logs/news_aggregator.log")
LOGGING_MESSAGE_FORMAT = "[%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(levelname)s] >> %(message)s"

EXECUTION_MODES = {"dev": "DEVELOPMENT", "prod": "PRODUCTION"}
