# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Tuple

from tornado.httputil import HTTPServerRequest

from api.base import APIRequestProcessor
from logic.login import LogIn


class LogInProcessor(APIRequestProcessor):

    def login(self, request: HTTPServerRequest) -> Tuple[int, dict]:
        return self.process_request(request, LogIn, are_body_args_allowed=True)
