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
"""
from select import select
from typing import Optional, Awaitable

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import define, parse_command_line, options
from tornado.web import RequestHandler, Application, HTTPError
from tornado.escape import json_encode

from api.catalog import CatalogProcessor
from api.login import LogInProcessor
from api.signup import SignUpProcessor
from api.subscriptions import SubscriptionsProcessor
from api.users import UsersProcessor
from db.connection import database_async_engine
from db.mapping.users import Sessions
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


class SignUpHandler(BaseRequestHandler):
    """
    This handler should not exist, originally the sign up method was going to be a POST in the Users handler,
    but Tornado is not fully compatible with specific URL patterns for handler methods (an URL pattern must match all
    handler methods, there are no distinctions)
    TODO: ¿Se puede cambiar esto último e incluir este endpoint en UsersHandler?
    """

    SUPPORTED_METHODS = ("POST",)

    def post(self):
        """User sign up"""
        processor = SignUpProcessor()
        status_code, service_response = processor.signup(self.request)

        self.set_status(status_code)
        self.write(json_encode(service_response))


class UsersHandler(BaseRequestHandler):

    SUPPORTED_METHODS = ("GET", "PUT", "DELETE")

    def __init__(self, *args, **kwargs):
        super(UsersHandler, self).__init__(*args, **kwargs)
        self._processor = UsersProcessor()

    def get(self, user_id: int):
        """User data: Personal information, subscriptions and interests"""
        status_code, service_response = self._processor.user_data(self.request,
                                                                  url_parameters={"user_id": int(user_id)})

        self.set_status(status_code)
        self.write(json_encode(service_response))

    def put(self, user_id: int):
        """User data modification"""
        status_code, service_response = self._processor.user_data_modification(self.request,
                                                                               url_parameters={"user_id": int(user_id)})

        self.set_status(status_code)
        self.write(json_encode(service_response))

    def delete(self, user_id: int):
        """User account deactivation"""
        status_code, service_response = self._processor.account_deactivation(self.request,
                                                                             url_parameters={"user_id": int(user_id)})

        self.set_status(status_code)
        self.write(json_encode(service_response))


class LoginHandler(BaseRequestHandler):
    # TODO: Añadir soporte para OAuth con Google: https://www.tornadoweb.org/en/stable/auth.html

    SUPPORTED_METHODS = ("POST",)

    def __init__(self, *args, **kwargs):
        super(LoginHandler, self).__init__(*args, **kwargs)
        self._processor = LogInProcessor()

    def post(self):
        """Login request"""
        status_code, service_response = self._processor.login(self.request)

        self.set_status(status_code)
        self.write(json_encode(service_response))


class SubscriptionsHandler(BaseRequestHandler):

    SUPPORTED_METHODS = ("GET", "POST", "PATCH", "DELETE")

    def __init__(self, *args, **kwargs):
        super(SubscriptionsHandler, self).__init__(*args, **kwargs)
        self._processor = SubscriptionsProcessor()

    def get(self, user_id: int):
        """Update subscriptions feeds"""
        # TODO: Mejorar para que use coroutines y tome los datos de forma asíncrona. Por ahora no funciona.
        status_code, service_response = self._processor.reload_news(self.request,
                                                                    url_parameters={"user_id": int(user_id)})

        self.set_status(status_code)
        self.write(json_encode(service_response))

    def post(self, user_id: int):
        """Create a new subscription for the given user"""
        status_code, service_response = self._processor.create_subscription(self.request,
                                                                            url_parameters={"user_id": int(user_id)})

        self.set_status(status_code)
        self.write(json_encode(service_response))

    def patch(self, user_id: int):
        """Order the subscriptions of a given user"""

        # TODO
        response = {
            "message": "SUBSCRIPTIONS -> PATCH",
            "params": {
                "user_id": user_id,
                "new_order": self.get_body_argument('new_order')
            }
        }

        self.write(response)

    def delete(self, user_id: int):
        """An user unsubscribes from a RSS feed"""
        status_code, service_response = self._processor.delete_subscription(self.request,
                                                                            url_parameters={"user_id": int(user_id)})

        self.set_status(status_code)
        self.write(json_encode(service_response))


class CatalogHandler(BaseRequestHandler):

    SUPPORTED_METHODS = ("GET",)

    def __init__(self, *args, **kwargs):
        super(CatalogHandler, self).__init__(*args, **kwargs)
        self._processor = CatalogProcessor()

    def get(self):
        """Get available RSS sites"""
        status_code, service_response = self._processor.get_rss_catalog(self.request)

        self.set_status(status_code)
        self.write(json_encode(service_response))


def session_expiration_task():
    """
    This function implements a session expiration check: Each time it gets invoked, every alive session is closed if
    it's alive time expires
    """
    async def asynchronous_database_fetch():

        alive_sessions_query = select(Sessions.id, Sessions.closing_date, Sessions.expiration_date, Sessions.is_alive).\
            where(Sessions.is_alive == True)

        async with database_async_engine.connect() as database_async_connection:
            alive_sessions = await database_async_connection.execute(alive_sessions_query).all()

        for alive_session in alive_sessions:
            print(alive_session.id, alive_session.is_alive, alive_session.expiration_date)

    # TODO: No debería instanciarse en cada ejecución, solucionar.
    AppLogger().logger.info(f"Session expiration task, result: {await asynchronous_database_fetch()}")


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
    IOLoop.instance().start()

    # Start the session expiration periodic task.
    periodic_session_expiration = PeriodicCallback(session_expiration_task, callback_time=30000)
    periodic_session_expiration.start()


if __name__ == '__main__':
    main()
