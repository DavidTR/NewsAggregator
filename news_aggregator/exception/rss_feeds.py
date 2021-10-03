# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from exception.base import BaseAppException


class RSSFeedDoesNotExist(BaseAppException):
    exception_code = "RSS-DOES-NOT-EXIST"

    _default_error_message = "The requested RSS Feed does not exist"

