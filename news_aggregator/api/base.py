# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
API request processor base class.

"""
from typing import Tuple

from tornado.httputil import HTTPServerRequest

from exception.api import MissingQueryStringArguments, MissingBodyArguments
from exception.base import BaseAppException
from logic.base import ServiceClassType


class BaseAPI:

    def _fetch_arguments(self, request: HTTPServerRequest, required_querystring_args: bool = False,
                         required_body_args: bool = False) -> dict:
        """
        Fetches the arguments depending on where to get them (querystring or body). Each API service will indicate
        the origin of its parameters, so as to not allow a querystring encoded argument list in a POST request,
        for example.
        """
        # The arguments will be returned in a dictionary.
        args = {}

        # Querystring and/or body arguments are loaded and parsed.
        if required_querystring_args:
            qs_args = request.arguments
            if not qs_args:
                raise MissingQueryStringArguments()
            args.update(qs_args)

        if required_body_args:
            body_args = request.body_arguments
            if not body_args:
                raise MissingBodyArguments()
            args.update(body_args)

        return args


    def process_request(self, request: HTTPServerRequest, service_class: ServiceClassType,
                        required_querystring_args: bool = False, required_body_args: bool = False) -> Tuple[int, dict]:
        """Processes a single request, executing the given service logic"""


        try:
            service_instance = service_class()
            service_parameters = self._fetch_arguments(request, required_querystring_args, required_body_args)
            signup.set_parameters(service_parameters)
            signup.validate_parameters()
            service_response = signup.execute()

            return service_response
        except BaseAppException as base_app_exception:
            pass
