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

from cfg import config
from db.connection import database_engine, database_async_engine, AsynchronousSession
from db.mapping.users import Users, Sessions
from logic.signup import SignUp
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
    async def asynchronous_database_fetch():

        alive_sessions_query = select(Sessions.id, Sessions.closing_date, Sessions.expiration_date, Sessions.is_alive). \
            where(Sessions.is_alive == True)

        async with database_async_engine.connect() as database_async_connection:
            alive_sessions_corotuine = await database_async_connection.execute(alive_sessions_query)
            alive_sessions = alive_sessions_corotuine.all()

        expired_sessions_ids = []
        for alive_session in alive_sessions:
            print(alive_session.id, alive_session.is_alive, alive_session.expiration_date, datetime.datetime.now())
            if alive_session.expiration_date <= datetime.datetime.now():
                expired_sessions_ids.append(alive_session.id)

        if expired_sessions_ids:
            # https://docs.sqlalchemy.org/en/14/core/dml.html#sqlalchemy.sql.expression.Update
            expire_sessions_query = update(Sessions).where(Sessions.id.in_(expired_sessions_ids)).values(is_alive=False).execution_options(synchronize_session="fetch")

            async with AsynchronousSession() as session:
                async with session.begin():
                    result = await database_async_connection.execute(expire_sessions_query)

            print(result)

        await database_async_engine.dispose()

    asyncio.run(asynchronous_database_fetch())


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
