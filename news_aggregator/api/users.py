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
from logic.user_data_modification import UserDataModification


class UsersProcessor(APIRequestProcessor):

    def user_data(self, request: HTTPServerRequest, url_parameters: dict) -> Tuple[int, dict]:
        return self.process_request(request, UserDataListing, url_parameters=url_parameters,
                                    are_querystring_args_allowed=True)

    def account_deactivation(self, request: HTTPServerRequest, url_parameters: dict) -> Tuple[int, dict]:
        return self.process_request(request, AccountDeactivation, url_parameters=url_parameters,
                                    are_body_args_allowed=True)

    def user_data_modification(self, request: HTTPServerRequest, url_parameters: dict) -> Tuple[int, dict]:
        return self.process_request(request, UserDataModification, url_parameters=url_parameters,
                                    are_body_args_allowed=True)


