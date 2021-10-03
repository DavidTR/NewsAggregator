# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Const values.

"""
import logging
import os
import sys
from pathlib import Path

# Parent directory of the current file, as we are inside the "const" package.
PROJECT_ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

MAX_INT_VALUE = sys.maxsize
MIN_INT_VALUE = -sys.maxsize - 1

LOGGING_MESSAGES_PATTERN = ""
LOGGING_MIN_LEVEL = logging.DEBUG
LOGGING_FILE_PATH = os.path.join(PROJECT_ROOT_PATH, "logs/news_aggregator.log")
LOGGING_MESSAGE_FORMAT = "[%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(levelname)s] >> %(message)s"
