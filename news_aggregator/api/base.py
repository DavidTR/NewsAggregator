# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
API request processor base class.

This class will handle the basic flow of requests and the possible errors that may occur while processing them. It uses
a subset of HTTP codes to deliver a meaningful response.

See: https://softwareengineering.stackexchange.com/q/341732/402704
"""
from typing import Tuple

from tornado.httputil import HTTPServerRequest

from exception.api import MissingQueryStringArguments, MissingBodyArguments, BaseAPIException
from exception.base import BaseAppException
from logic.base import ServiceClassType


class APIRequestProcessor:

    @staticmethod
    def _fetch_arguments(request: HTTPServerRequest, required_querystring_args: bool = False,
                         required_body_args: bool = False) -> dict:
        """
        Fetches the arguments depending on where to get them (querystring or body). Each API service will indicate
        the origin of its parameters, so as to not allow a querystring encoded argument list in a POST request,
        for example.

        TODO: Agregar soporte para ficheros.
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
        # By default, suppose that the request is processed correctly.
        status_code = 200

        # Basic service response
        service_response = self._service_response()

        try:
            service_instance = service_class()
            service_parameters = self._fetch_arguments(request, required_querystring_args, required_body_args)
            service_instance.set_parameters(service_parameters)
            service_instance.validate_parameters()
            service_response["data"] = service_instance.execute()

        # This order must be maintained: as all exceptions inherit from BaseAppException, except blocks capturing
        # exceptions from this class must be the lasts in every try block.
        # TODO: Esto cambiará en un futuro, actualizar comentario.
        except BaseAPIException as api_exception:
            # Deal with API errors.
            service_response["error"] = {
                "code": api_exception.exception_code,
                "message": api_exception.error_message
            }

            # If an API error occurs, a 400 status code is returned, as the client request is malformed in some way.
            status_code = 400

        except BaseAppException as app_exception:
            # Deal with business logic errors.
            service_response["error"] = {
                "code": app_exception.exception_code,
                "message": app_exception.error_message
            }
            # TODO: SET STATUS CODE

        return status_code, service_response

    @staticmethod
    def _service_response() -> dict:
        """Default response"""
        return {"data": {}}
