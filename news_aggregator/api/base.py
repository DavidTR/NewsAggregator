# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
API request processor base class.

This class will handle the basic flow of requests and the possible errors that may occur while processing them. It uses
a subset of HTTP codes to deliver a meaningful response.

See: https://softwareengineering.stackexchange.com/q/341732/402704
"""
import urllib.parse
from typing import Tuple

from sqlalchemy import select
from tornado import escape
from tornado.httputil import HTTPServerRequest

from db.connection import database_engine
from db.mapping.users import Sessions
from exception.api import UnableToParseArguments
from exception.base import BaseAppException
from exception.sessions import SessionDoesNotExist, SessionIsNotAlive
from logic.base import ServiceClassType
from util.logging import AppLogger
from util.util import fast_list_flattener


class APIRequestProcessor:

    def __init__(self):
        """Initializes an instance of this class"""
        # Easier access to the logger for internal use of all API processor classes.
        self._logger = AppLogger().logger

    def _fetch_arguments(self, request: HTTPServerRequest, are_querystring_args_allowed: bool = False,
                         are_body_args_allowed: bool = False) -> dict:
        """
        Fetches the arguments depending on where to get them (querystring or body). Each API service will indicate
        the origin of its parameters, so as to not allow a querystring encoded argument list in a POST request,
        for example.

        TODO: Agregar soporte para ficheros.
        TODO: Limitar los parámetros reconocidos por servicio. Es decir, utilizar la lista
         _parameters_constraints para capturar únicamente los parámetros esperados, teniendo en cuenta
         si es o no opcional y su tipo. En definitiva, pasar toda la lógica de gestión de parámetros aquí.
        """
        # The arguments will be returned in a dictionary.
        args = {}

        # Querystring and/or body arguments are loaded and parsed.
        try:
            if are_querystring_args_allowed:
                qs_args = urllib.parse.parse_qs(request.query, encoding='utf-8')
                # parse_qs (which is the same function the tornado escape.parse_qs_bytes uses internally) returns
                # a list of values for every parameter (even if only one value is provided), only the last provided
                # value will be chosen.
                for name, value in qs_args.items():
                    qs_args[name] = qs_args[name][-1]
                args.update(qs_args)

            if are_body_args_allowed:
                body_args = escape.json_decode(request.body)
                args.update(body_args)
        except Exception as args_parse_exception:
            # This Exception broad except block is permitted by PEP8 as long as the exception data is logged.
            # See: https://pep8.org/#programming-recommendations
            self._logger.exception(f"An error occurred while loading the request arguments: {args_parse_exception}")
            raise UnableToParseArguments()

        return args

    def process_request(self, request: HTTPServerRequest, service_class: ServiceClassType, url_parameters: dict = None,
                        are_querystring_args_allowed: bool = False,
                        are_body_args_allowed: bool = False) -> Tuple[int, dict]:
        """Processes a single request, executing the given service logic"""
        # By default, suppose that the request gets processed correctly.
        status_code = 200

        service_response = self._service_response()

        try:
            service_parameters = self._fetch_arguments(request, are_querystring_args_allowed, are_body_args_allowed)
            service_instance = service_class()

            # URL arguments have more priority than QS or body arguments.
            if url_parameters:
                service_parameters.update(url_parameters)

            service_instance.set_parameters(service_parameters)
            service_instance.validate_parameters()

            # There's no need for certain services to require a session ID (catalog for example), so this check can be
            # ignored if needed.
            service_instance.check_session()
            service_response["data"] = service_instance.service_logic()

        # This order must be maintained: as all exceptions inherit from BaseAppException, except blocks capturing
        # exceptions from this class must be the lasts in every try block.
        # TODO: Esto cambiará en un futuro, actualizar comentario.
        except BaseAppException as exception:
            # Deal with API and business logic errors. For now they're managed in the same way, there is no need to
            # duplicate code.
            self._logger.exception(f"An expected error has occurred while executing the service "
                                   f"{service_class.__name__}")

            service_response["error"] = {
                "code": exception.exception_code,
                "message": exception.error_message
            }

            # Depending on the error, a specific HTTP status code will be returned, so as to be as informative to the
            # user as possible.
            status_code = exception.http_status_code

            recommendation_message = exception.recommendation_message
            if recommendation_message:
                service_response["error"]["recommendation"] = recommendation_message

        return status_code, service_response

    @staticmethod
    def _service_response() -> dict:
        """Default response"""
        return {"data": {}}
