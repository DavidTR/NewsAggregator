# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Main project file, which will run the server loop.

If this program is run with the "--help" argument, it prints all the supported options that can be set via command line.
Execute python news_aggregator.py --help to the see the supported options.

TODO: Agregar parámetros de login OAUTH a cada petición para securizarlas. Usar TLS. Usar data_received y streams,
 usar peticiones asíncronas.
"""
from typing import Optional, Awaitable, Any

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options
from tornado.web import RequestHandler, Application, HTTPError
from tornado.escape import json_encode

from api.signup import SignUpProcessor
from api.users import UsersProcessor


class BaseRequestHandler(RequestHandler):

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

    def get(self, user_id: int):
        """User data: Personal information, subscriptions and interests"""
        processor = UsersProcessor()
        status_code, service_response = processor.user_data(self.request)

        self.set_status(status_code)
        self.write(json_encode(service_response))

    def put(self, user_id: int):
        """User data modification"""

        if self.request.body_arguments:
            response = {
                "message": f"USERS -> PUT ({user_id})",
                "params": {
                    "name": self.get_body_argument('name', default=None),
                    "surname": self.get_body_argument('surname', default=None),
                    "email": self.get_body_argument('email', default=None)
                }
            }

            self.write(response)
        else:
            raise HTTPError(400)

    def delete(self, user_id: int):
        """User account deactivation"""
        self.write(f"USERS -> DELETE ({user_id})")


class LoginHandler(BaseRequestHandler):

    SUPPORTED_METHODS = ("POST",)

    def post(self):
        """Login request"""
        if self.request.body_arguments:
            response = {
                "message": "LOGIN -> POST",
                "params": {
                    "email": self.get_body_argument('email'),
                    "password": self.get_body_argument('password')
                }
            }

            self.write(response)
        else:
            raise HTTPError(400)


class SubscriptionsHandler(BaseRequestHandler):

    SUPPORTED_METHODS = ("GET", "POST", "PATCH", "DELETE")

    def get(self, user_id: int):
        """Update subscriptions feeds"""
        response = {
            "message": "SUBSCRIPTIONS -> GET",
            "params": {
                "user_id": user_id,
                "rss_feeds_ids": self.get_argument("rss_feeds_ids", default=None)
            }
        }

        self.write(response)

    def post(self, user_id: int):
        """Create a new subscription for the given user"""
        response = {
            "message": "SUBSCRIPTIONS -> POST",
            "params": {
                "user_id": user_id,
                "rss_feed_id": self.get_body_argument('rss_feed_id')
            }
        }

        self.write(response)

    def patch(self, user_id: int):
        """Order the subscriptions of a given user"""
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
        response = {
            "message": "SUBSCRIPTIONS -> DELETE",
            "params": {
                "user_id": user_id,
                "rss_feed_id_list": self.get_body_argument('rss_feed_id_list')
            }
        }

        self.write(response)


class CatalogHandler(BaseRequestHandler):

    SUPPORTED_METHODS = ("GET",)

    def get(self):
        response = {
            "message": "CATALOG -> GET",
            "params": {
                "tag_id": self.get_argument("tag_id", default=None)
            }
        }

        self.write(response)


def main():
    def make_handlers() -> list:
        """Creates the list of handlers for the tornado app"""
        handlers = [
            (r"/v01/users/?", SignUpHandler),
            (r"/v01/users/([0-9]+)/?", UsersHandler),
            (r"/v01/login/?", LoginHandler),
            (r"/v01/subscriptions/([0-9]+)/?", SubscriptionsHandler),
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


if __name__ == '__main__':
    main()
