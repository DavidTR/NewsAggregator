# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Mapping classes for rss feeds-oriented tables. See db/mapping/__init__.py for more information.

"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKeyConstraint, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship

from db.mapping import MappingBaseClass


class RSSFeedsNews(MappingBaseClass):
    """
    News obtained from the RSS sites stored in the "rss_feeds" table. Every row in this table will hold all the news
    received from a RSS feed in a given date. This information will be used as:
        1. Cache to avoid calls to news sites made by different users in a short period of time.
        2. Store a history of news for later use (maybe as a library of some kind).
    """
    __tablename__ = "rss_feeds_news"

    id = Column(Integer, autoincrement=True, primary_key=True)
    rss_feed_id = Column(Integer, ForeignKey("rss_feeds.id", name="rss_feeds_news_rss_feeds_id_fk", ondelete="CASCADE"), nullable=False)
    query_date = Column(DateTime)
    news_data = Column(JSON)


class RSSFeeds(MappingBaseClass):
    """Sites that expose their news using RSS"""
    __tablename__ = "rss_feeds"

    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String(50), nullable=False, unique=True)
    title = Column(String(100))
    news = relationship(RSSFeedsNews)


class RSSFeedsTags(MappingBaseClass):
    """
    Relationship between RSS sites and tags. Each RSS site may have more than one tag, giving information about the type
     of content they publish to potential subscribers
    """
    __tablename__ = "rss_feeds_tags"

    rss_feed_id = Column(Integer, ForeignKey("rss_feeds.id", name="rss_feeds_tags_rss_feeds_id_fk", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", name="rss_feeds_tags_tags_id_fk", ondelete="CASCADE"), primary_key=True)
