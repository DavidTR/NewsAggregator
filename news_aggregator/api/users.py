# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Tuple

from tornado.httputil import HTTPServerRequest

from api.base import APIRequestProcessor
from logic.account_deactivation import AccountDeactivation
from logic.user_data_listing import UserDataListing


class UsersProcessor(APIRequestProcessor):

    def user_data(self, request: HTTPServerRequest, url_parameters: dict) -> Tuple[int, dict]:
        return self.process_request(request, UserDataListing, url_parameters=url_parameters)

    def account_deactivation(self, request: HTTPServerRequest, url_parameters: dict) -> Tuple[int, dict]:
        return self.process_request(request, AccountDeactivation, url_parameters=url_parameters)
