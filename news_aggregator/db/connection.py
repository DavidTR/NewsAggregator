# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------
TODO: Rehacer documentación para el cambio del motor asíncrono.

Database connection session instance that will be used all over the application when needed.

The session will be created by the method scoped_session, which

See:
    - https://docs.sqlalchemy.org/en/14/orm/contextual.html
    - https://docs.sqlalchemy.org/en/14/orm/session_basics.html
    - https://docs.sqlalchemy.org/en/14/orm/session.html
    - https://docs.sqlalchemy.org/en/14/core/connections.html
    - https://docs.sqlalchemy.org/en/14/core/connections.html?highlight=engine#module-sqlalchemy.engine

"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from cfg import config
from util.design_patterns import SingletonMetaclass


class DatabaseEngines(metaclass=SingletonMetaclass):
    """
    Creates the engines, establishing connection to the database. This function will be called only once, as there must
     be only one engine of each type, which lifespan is tied to the application that uses it. This is the most efficient
     way to use it, as can be seen in the documentation: https://docs.sqlalchemy.org/en/14/core/connections.html.

     The Singleton metaclass manages ensures that only one instance of this class (and hence, only one database engine)
     is created.
    """

    def __init__(self, *args, **kwargs):
        super(DatabaseEngines, self).__init__(*args, **kwargs)

        database_connection_settings = config.settings.DATABASE_CONNECTION
        self._sync_engine = create_engine(f'mysql://{database_connection_settings["uid"]}'
                                          f':{database_connection_settings["pwd"]}'
                                          f'@{database_connection_settings["server"]}'
                                          f'/{database_connection_settings["database"]}')

        self._async_engine = create_async_engine(f'mysql+aiomysql://{database_connection_settings["uid"]}'
                                                 f':{database_connection_settings["pwd"]}'
                                                 f'@{database_connection_settings["server"]}'
                                                 f'/{database_connection_settings["database"]}')

    def get_database_sync_engine(self):
        """Returns the database connection synchronous engine"""
        return self._sync_engine

    def get_database_async_engine(self):
        """Returns the database connection asynchronous engine"""
        return self._async_engine


"""
Construct Session instances with the sessionmaker factory and ensure that there will not be any data corruption
with scoped_session. scoped_session implements the registry pattern and, along with thread local storage, makes
that every thread that requests it can have an unique Session object, held in the thread's local storage, providing
thread safety to ORM sessions.
See: https://docs.sqlalchemy.org/en/14/orm/contextual.html?highlight=scoped_session#thread-local-scope

As it will be implemented in this application -for safety and inconsistency prevention reasons- the sessions and
transactions must be created and opened, respectively, for each web request. When finished processing the request,
the transaction will be closed (committed or rolled back) and the session will be closed (in this case, removed).
See: https://docs.sqlalchemy.org/en/14/orm/contextual.html?highlight=scoped_session#using-thread-local-scope-with-web
-applications
"""

# As this instance is global, any other method or function can also get and use the engine.
database_engines = DatabaseEngines()

database_engine = database_engines.get_database_sync_engine()
Session = scoped_session(sessionmaker(bind=database_engine))

database_async_engine = database_engines.get_database_async_engine()
AsynchronousSession = sessionmaker(database_async_engine, expire_on_commit=False, class_=AsyncSession)
