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


class SignUpHandler(RequestHandler):
    """This handler should not exist, originally the sign up method was going to be a POST in the Users handler,
    but Tornado is not fully compatible with """

    SUPPORTED_METHODS = ("POST",)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        """User sign up"""
        # TESTS ## TESTS ## TESTS ## TESTS ## TESTS ## TESTS ## TESTS #
        if self.request.body_arguments:
            from logic.signup import SignUp

            signup = SignUp()
            service_parameters = dict(name=self.get_body_argument("name", default=None),
                                      surname=self.get_body_argument("surname", default=None),
                                      email=self.get_body_argument("email", default=None),
                                      password=self.get_body_argument("password", default=None))
            signup.set_parameters(service_parameters)
            signup.validate_parameters()
            service_response = signup.execute()

            return service_response
        else:
            # Instead of returning a 500 error code, if no body arguments are given, a 400 code (Bad Request) is
            # returned.
            raise HTTPError(400)
        # TESTS ## TESTS ## TESTS ## TESTS ## TESTS ## TESTS ## TESTS #


class UsersHandler(RequestHandler):

    SUPPORTED_METHODS = ("GET", "PUT", "DELETE")

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        print(kwargs)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self, user_id: int):
        """User data: Personal information, subscriptions and interests"""
        self.write(f"USERS -> GET ({user_id})")

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


class LoginHandler(RequestHandler):

    SUPPORTED_METHODS = ("POST",)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

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


class SubscriptionsHandler(RequestHandler):

    SUPPORTED_METHODS = ("GET", "POST", "PATCH", "DELETE")

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        """This handler should use this to create streams of news (see get method)"""
        pass

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


class CatalogHandler(RequestHandler):

    SUPPORTED_METHODS = ("GET",)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

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
