# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Tuple

from tornado.httputil import HTTPServerRequest

from api.base import APIRequestProcessor
from logic.signup import SignUp


class SignUpProcessor(APIRequestProcessor):

    def signup(self, request: HTTPServerRequest) -> Tuple[int, dict]:
        return self.process_request(request, SignUp, are_body_args_required=True)
