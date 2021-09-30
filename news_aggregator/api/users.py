# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Tuple

from tornado.httputil import HTTPServerRequest

from api.base import APIRequestProcessor
from logic.users import UserData


class UsersProcessor(APIRequestProcessor):

    def user_data(self, request: HTTPServerRequest) -> Tuple[int, dict]:
        return self.process_request(request, UserData, are_body_args_required=True)
