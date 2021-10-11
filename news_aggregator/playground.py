# -*- encoding:utf-8 -*-
import asyncio
import datetime
import string
import time
import uuid
from base64 import urlsafe_b64encode
from math import trunc
from string import ascii_uppercase

import bcrypt
import feedparser
import pyodbc
import pytz
from sqlalchemy.sql import select, update
from tornado import gen
from tornado.ioloop import IOLoop

from cfg import config
from db.connection import database_engine, database_async_engine, AsynchronousSession
from db.mapping.users import Users, Sessions
from logic.signup import SignUp
from periodic.session_expiration import async_session_expiration
from util.logging import AppLogger

"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Playground file used to test frameworks, modules, code snippets and more.

"""


def feedparser_stuff() -> None:
    """Feedparser module simple tests"""
    bbc_rss_feed = feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")

    for entry in bbc_rss_feed.entries:
        print(entry)


def mysql_stuff() -> None:
    database_connection_settings = config.settings.DATABASE_CONNECTION
    connection_string = (
        f'DRIVER={database_connection_settings["driver"]};'
        f'SERVER={database_connection_settings["server"]};'
        f'DATABASE={database_connection_settings["database"]};'
        f'UID={database_connection_settings["uid"]};'
        f'PWD={database_connection_settings["pwd"]};'
        f'charset={database_connection_settings["charset"]};'
    )
    # print(pyodbc.drivers())
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print(cursor.service_logic("SELECT * FROM tags;").fetchall())


def timezone_stuff() -> None:
    """Python UTC and timezones example code snippets"""

    # The datetime objects should be stored in UTC in the database, along with the timezone (in a different column).
    # Whenever needed, the date and the timezone should be fetched from the database to construct the datetime object
    # as needed.

    # The following lines create a UTC localized time (with timezone) that holds the present time in UTC.
    utc_timezone = pytz.timezone('UTC')
    now = utc_timezone.localize(datetime.datetime.utcnow())

    print(f"UTC time: {now}")

    # This is the timezone string that should be stored in the database
    # (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
    # If the present time needs to be formatted with a timezone:
    madrid_timezone = pytz.timezone('Europe/Madrid')
    madrid_local_time = now.astimezone(madrid_timezone)

    print(f"Madrid local time: {madrid_local_time}")

    # These lines already consider DST, which can be checked by calling the "dst()" method. This method outputs the
    # number of ours (positive or negative) with respect to UTC applied to the date object as DST.
    print(f"Madrid local time DST: {madrid_local_time.dst()}")


def string_stuff(test_string: str) -> None:
    """String stuff"""
    print(any(map(str.isupper, test_string)))

    if not isinstance(test_string, str) and ascii_uppercase:
        print("No capital letter in test_string")

    special = string.punctuation

    sum([character in test_string for character in list(special)])


def sqlalchemy_stuff() -> None:
    """SQLAlchemy stuff"""
    users = select(Users).where(Users.email == 'test@test.com')

    with database_engine.connect() as database_connection:
        print(database_connection.execute(users).first())


def bcrypt_stuff():
    """Bcrypt stuff"""
    # Bcrypt works with bytes strings, in order to generate a byte string from a conventional one, use the method
    # "encode".
    valid_password_example = "TESTTEST;?:-".encode(encoding='UTF-8')
    print(valid_password_example)

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(valid_password_example, salt)
    print(salt)
    print(hashed_password)

    # Check if the password example matches the generated value. hashed_password has the generated salt as a prefix.
    if bcrypt.checkpw(valid_password_example, hashed_password):
        print("Match!")
    else:
        print("No match!")


def signup_stuff() -> None:
    signup = SignUp()
    service_parameters = dict(name='Test 5', surname='Test Test', email='test5@test.com', password='TESTTEST;?:-')
    signup.set_parameters(service_parameters)
    signup.validate_parameters()
    signup.service_logic()


def logging_stuff() -> None:
    AppLogger().logger.info("TEST  ^?¿¡'123-.-.;^$·%$!/€@ł€@łßðæßß“ł€ħ”€@¶ħðđħ↓←ŧ€↓ðđħ¶↓¶ŋn")


def sessions_stuff() -> None:
    for i in range(1, 30):
        user_id = 1
        timestamp = trunc(time.time())
        salt = f"{user_id}-{timestamp}"
        random_uuid_hex = uuid.uuid4().hex
        session_id1 = salt + random_uuid_hex
        session_id = urlsafe_b64encode(session_id1.encode()).decode('utf-8')

        print(session_id)


def sessions_expiration_stuff():
    asyncio.run(async_session_expiration())


if __name__ == '__main__':
    # feedparser_stuff()
    # mysql_stuff()
    # timezone_stuff()
    # string_stuff("A2BF/?!;:cdefgh")
    # sqlalchemy_stuff()
    # bcrypt_stuff()
    # signup_stuff()
    # logging_stuff()
    sessions_expiration_stuff()
