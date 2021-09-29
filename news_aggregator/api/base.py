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

from tornado import escape
from tornado.httputil import HTTPServerRequest

from exception.api import MissingQueryStringArguments, MissingBodyArguments, BaseAPIException, UnableToParseArguments
from exception.base import BaseAppException
from logic.base import ServiceClassType


class APIRequestProcessor:

    @staticmethod
    def _fetch_arguments(request: HTTPServerRequest, are_querystring_args_required: bool = False,
                         are_body_args_required: bool = False) -> dict:
        """
        Fetches the arguments depending on where to get them (querystring or body). Each API service will indicate
        the origin of its parameters, so as to not allow a querystring encoded argument list in a POST request,
        for example.

        TODO: Agregar soporte para ficheros.
        """
        # The arguments will be returned in a dictionary.
        args = {}

        # Querystring and/or body arguments are loaded and parsed.
        try:
            if are_querystring_args_required:
                qs_args = escape.parse_qs_bytes(request.query)
                if not qs_args:
                    raise MissingQueryStringArguments()
                args.update(qs_args)

            if are_body_args_required:
                body_args = escape.json_decode(request.body)
                if not body_args:
                    raise MissingBodyArguments()
                args.update(body_args)
        except Exception as args_parse_exception:
            # This Exception broad except block is permitted by PEP8 as long as the exception data is logged.
            # See: https://pep8.org/#programming-recommendations
            # TODO: Log de la excepción.
            raise UnableToParseArguments()

        return args

    def process_request(self, request: HTTPServerRequest, service_class: ServiceClassType,
                        are_querystring_args_required: bool = False,
                        are_body_args_required: bool = False) -> Tuple[int, dict]:
        """Processes a single request, executing the given service logic"""
        # By default, suppose that the request gets processed correctly.
        status_code = 200

        service_response = self._service_response()

        try:
            service_instance = service_class()
            service_parameters = self._fetch_arguments(request, are_querystring_args_required, are_body_args_required)
            service_instance.set_parameters(service_parameters)
            service_instance.validate_parameters()
            service_response["data"] = service_instance.execute()

        # This order must be maintained: as all exceptions inherit from BaseAppException, except blocks capturing
        # exceptions from this class must be the lasts in every try block.
        # TODO: Esto cambiará en un futuro, actualizar comentario.
        except BaseAppException as exception:
            # Deal with API and business logic errors. For now their managed in the same way, there is no need to
            # duplicate code.
            service_response["error"] = {
                "code": exception.exception_code,
                "message": exception.error_message
            }

            status_code = exception.http_status_code

            recommendation_message = exception.recommendation_message
            if recommendation_message:
                service_response["error"]["recommendation"] = recommendation_message

        return status_code, service_response

    @staticmethod
    def _service_response() -> dict:
        """Default response"""
        return {"data": {}}