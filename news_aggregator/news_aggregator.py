# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Main project file, which will run the server loop.

If this program is run with the "--help" argument, it prints all the supported options that can be set via command line.
Execute python news_aggregator.py --help to the see the supported options.

TODO: Agregar parámetros de login OAUTH a cada petición para securizarlas. Usar TLS. Usar data_received y streams,
 usar peticiones asíncronas.
TODO: Mover el tratamiento de tipos de argumentos URL a los procesadores, que también se encargarán de validar los
 tipos y formatos de parámetros. Así no será necesario hacer un casting aquí.
TODO: Documentar usando :arg y :return, al menos en clases base. Así se explicará qué hace cada argumento.
"""
import time
from typing import Optional, Awaitable

from tornado.escape import json_encode
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options
from tornado.web import RequestHandler, Application

from api.catalog import CatalogProcessor
from api.login import LogInProcessor
from api.signup import SignUpProcessor
from api.subscriptions import SubscriptionsProcessor
from api.users import UsersProcessor
from periodic.session_expiration import async_session_expiration
from util.logging import AppLogger


class BaseRequestHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseRequestHandler, self).__init__(*args, **kwargs)

        # Easier access to the logger for internal use of all handler classes.xbo
        self._logger = AppLogger().logger

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def _handle_request(self, processor_method, *processor_args, **processor_kwargs):
        """Handles a request by invoking the fitting processor method"""
        request_start_time = time.perf_counter()
        status_code, service_response = processor_method(self.request, *processor_args, **processor_kwargs)

        service_response["elapsed"] = time.perf_counter() - request_start_time

        self.set_status(status_code)
        self.write(json_encode(service_response))


class SignUpHandler(BaseRequestHandler):
    """
    This handler should not exist, originally the sign up method was going to be a POST in the Users handler,
    but Tornado is not fully compatible with specific URL patterns for handler methods (an URL pattern must match all
    handler methods, there are no distinctions)
    TODO: ¿Se puede cambiar esto último e incluir este endpoint en UsersHandler?
    """

    SUPPORTED_METHODS = ("POST",)

    def __init__(self, *args, **kwargs):
        super(SignUpHandler, self).__init__(*args, **kwargs)
        self._processor = SignUpProcessor()

    def post(self):
        """User sign up"""
        self._handle_request(self._processor.signup)


class UsersHandler(BaseRequestHandler):
    SUPPORTED_METHODS = ("GET", "PUT", "DELETE")

    def __init__(self, *args, **kwargs):
        super(UsersHandler, self).__init__(*args, **kwargs)
        self._processor = UsersProcessor()

    def get(self, user_id: int):
        """User data: Personal information, subscriptions and interests"""
        self._handle_request(self._processor.user_data, url_parameters={"user_id": int(user_id)})

    def put(self, user_id: int):
        """User data modification"""
        self._handle_request(self._processor.user_data_modification, url_parameters={"user_id": int(user_id)})

    def delete(self, user_id: int):
        """User account deactivation"""
        self._handle_request(self._processor.account_deactivation, url_parameters={"user_id": int(user_id)})


class LoginHandler(BaseRequestHandler):
    # TODO: Añadir soporte para OAuth con Google: https://www.tornadoweb.org/en/stable/auth.html

    SUPPORTED_METHODS = ("POST",)

    def __init__(self, *args, **kwargs):
        super(LoginHandler, self).__init__(*args, **kwargs)
        self._processor = LogInProcessor()

    def post(self):
        """Login request"""
        self._handle_request(self._processor.login)


class SubscriptionsHandler(BaseRequestHandler):
    SUPPORTED_METHODS = ("GET", "POST", "PATCH", "DELETE")

    def __init__(self, *args, **kwargs):
        super(SubscriptionsHandler, self).__init__(*args, **kwargs)
        self._processor = SubscriptionsProcessor()

    def get(self, user_id: int):
        """Update subscriptions feeds"""
        # TODO: Mejorar para que use coroutines y tome los datos de forma asíncrona. Por ahora no funciona.
        self._handle_request(self._processor.reload_news, url_parameters={"user_id": int(user_id)})

    def post(self, user_id: int):
        """Create a new subscription for the given user"""
        self._handle_request(self._processor.create_subscription, url_parameters={"user_id": int(user_id)})

    def patch(self, user_id: int):
        """Order the subscriptions of a given user"""
        self._handle_request(self._processor.reorder_subscriptions, url_parameters={"user_id": int(user_id)})

    def delete(self, user_id: int):
        """An user unsubscribes from a RSS feed"""
        self._handle_request(self._processor.delete_subscription, url_parameters={"user_id": int(user_id)})


class CatalogHandler(BaseRequestHandler):
    SUPPORTED_METHODS = ("GET",)

    def __init__(self, *args, **kwargs):
        super(CatalogHandler, self).__init__(*args, **kwargs)
        self._processor = CatalogProcessor()

    def get(self):
        """Get available RSS sites"""
        self._handle_request(self._processor.get_rss_catalog)


def main():
    def make_handlers() -> list:
        """Creates the list of handlers for the tornado app"""

        handlers = [
            (r"/v01/users/?", SignUpHandler),
            (r"/v01/users/([0-9]+)/?", UsersHandler),
            (r"/v01/login/?", LoginHandler),
            (r"/v01/users/([0-9]+)/subscriptions/?", SubscriptionsHandler),
            (r"/v01/catalog/?", CatalogHandler)
        ]

        return handlers

    # For an option to be used, it must be defined first. This line is, hence, required if we want to be able to use a
    # custom port (in this case).
    define("port", default=8000, help="Run on the given port", type=int)

    # Parses the command line arguments and takes the supported tornado ones to configure the server. The arguments
    # must be passed like so: --option=value. If an option is not supported, it's returned by this method.
    # See https://www.tornadoweb.org/en/stable/options.html
    parse_command_line()

    app = Application(handlers=make_handlers())
    http_server = HTTPServer(app)
    http_server.listen(options.port)

    ioloop = IOLoop.current()

    # Start the session expiration periodic task.
    ioloop.add_callback(async_session_expiration)

    # Start the main loop, hence the web server.
    ioloop.start()


if __name__ == '__main__':
    main()
