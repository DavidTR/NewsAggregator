# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
Mapping classes for user-oriented tables. See db/mapping/__init__.py for more information.

"""
import datetime

from sqlalchemy import Column, Integer, String, Boolean, PrimaryKeyConstraint, ForeignKeyConstraint, DateTime

from db.mapping import MappingBaseClass


class Users(MappingBaseClass):
    """Signed up users in the application"""
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False)


class Subscriptions(MappingBaseClass):
    """Users subscribed to RSS feeds"""
    __tablename__ = "subscriptions"

    user_id = Column(Integer, primary_key=True)
    rss_feed_id = Column(Integer, primary_key=True)
    ForeignKeyConstraint(("user_id",), ("users.id",), name="subscriptions_users_id_fk", ondelete="CASCADE")
    ForeignKeyConstraint(("rss_feed_id",), ("rss_feeds.id",), name="subscriptions_rss_feeds_id_fk", ondelete="CASCADE")


class Sessions(MappingBaseClass):
    """All the sessions that users create when they log-in will be stored here"""
    __tablename__ = "sessions"

    id = Column(Integer, index=True, autoincrement=True, primary_key=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(String(100), nullable=False, unique=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    expiration_date = Column(DateTime, nullable=False)
    closing_date = Column(DateTime)
    is_alive = Column(Boolean, nullable=False, default=True)
    ForeignKeyConstraint(("user_id",), ("users.id",), name="sessions_users_id_fk", ondelete="CASCADE")
