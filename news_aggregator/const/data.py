# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Const values.

"""
import logging
import sys
from pathlib import Path

MAX_INT_VALUE = sys.maxsize
MIN_INT_VALUE = -sys.maxsize - 1

LOGGING_MESSAGES_PATTERN = ""
LOGGING_MIN_LEVEL = logging.DEBUG
# TEST ONLY
LOGGING_FILE_PATH = Path(f'{Path.cwd()}/logs/news_aggregator.log')
# LOGGING_FILE_PATH = Path(f'{Path.cwd()}/../logs/news_aggregator.log')
LOGGING_MESSAGE_FORMAT = "[%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(levelname)s] >> %(message)s"
