# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
from typing import Tuple

from tornado.httputil import HTTPServerRequest

from api.base import APIRequestProcessor
from logic.create_subscription import CreateSubscription
from logic.delete_subscription import DeleteSubscription
from logic.reload_news import ReloadNews
from logic.reorder_subscriptions import ReorderSubscriptions


class SubscriptionsProcessor(APIRequestProcessor):

    def create_subscription(self, request: HTTPServerRequest, url_parameters: dict) -> Tuple[int, dict]:
        return self.process_request(request, CreateSubscription, are_body_args_allowed=True,
                                    url_parameters=url_parameters)

    def delete_subscription(self, request: HTTPServerRequest, url_parameters: dict) -> Tuple[int, dict]:
        return self.process_request(request, DeleteSubscription, are_body_args_allowed=True,
                                    url_parameters=url_parameters)

    def reload_news(self, request: HTTPServerRequest, url_parameters: dict) -> Tuple[int, dict]:
        return self.process_request(request, ReloadNews, url_parameters=url_parameters,
                                    are_querystring_args_allowed=True)

    def reorder_subscriptions(self, request: HTTPServerRequest, url_parameters: dict) -> Tuple[int, dict]:
        return self.process_request(request, ReorderSubscriptions, url_parameters=url_parameters,
                                    are_body_args_allowed=True)
