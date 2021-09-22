# -*- encoding:utf-8 -*-
import datetime

import feedparser
import pyodbc
import pytz

from cfg import config
from exception.base import BaseAppException

"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Playground file used to test frameworks, modules, code snippets and more.

"""


def feedparser_test() -> None:
    """Feedparser module simple tests"""
    bbc_rss_feed = feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")

    for entry in bbc_rss_feed.entries:
        print(entry)


def mysql_connection() -> None:

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
    print(cursor.execute("SELECT * FROM tags;").fetchall())


def timezones() -> None:
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


class C1(BaseAppException):
    pass


class C2(BaseAppException):
    pass


if __name__ == '__main__':
    # feedparser_test()
    # mysql_connection()
    timezones()
