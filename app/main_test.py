# -*- encoding:utf-8 -*-
import feedparser

"""
             - File description -
----------------------------------------------
Playground file used to test frameworks,
modules, code snippets and such.

               - Activity log -
==============================================
2021/09/08 - David Téllez Rodríguez - Creation

"""

if __name__ == '__main__':
    bbc_rss_feed = feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")

    for entry in bbc_rss_feed.entries:
        print(entry)
