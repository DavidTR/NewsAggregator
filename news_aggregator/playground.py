# -*- encoding:utf-8 -*-
import feedparser
import pyodbc

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
    connection_string = (
        r'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
        r'SERVER=localhost;'
        r'DATABASE=NewsAggregator;'
        r'UID=news_aggregator;'
        r'PWD=news_aggregator;'
        r'charset=utf8mb4;'
    )
    # print(pyodbc.drivers())
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print(cursor.execute("SELECT * FROM tags;").fetchall())


if __name__ == '__main__':
    # feedparser_test()
    mysql_connection()
