# -*- encoding:utf-8 -*-
"""
                                                  - File description -
------------------------------------------------------------------------------------------------------------------------

"""
import datetime

from sqlalchemy import select, update
from tornado import gen

from cfg import config
from db.connection import database_async_engine, AsynchronousSession
from db.mapping.users import Sessions
from util.logging import AppLogger


async def async_session_expiration():
    """
    Retrieves alive sessions and expires them if required. This task is designed to work with Tornado's IOLoop like
    so (see news_aggregator.py:main):

        ioloop = IOLoop.current()

        # Start the session expiration periodic task.
        ioloop.add_callback(async_session_expiration)
        ioloop.start()

    It's very important that the previous sentences get executed in the given order, if the task is added after the
    server starts, the task will not be executed.
    """

    # TODO: Esta primera implementación funciona, pero puede dejar de funcionar por cualquier excepción, habiendo que
    #  reiniciar el backend completo para volver a encolarla. Lo más adecuado es usar un gestor de colas que lo haga
    #  automáticamente. Ver: Gestión de errores en tareas en segundo plano y reinicio automático con Tornado,
    #  y Celery como versión dos para este tipo de funcionalidad.

    task_config = config.settings.BACKGROUND_SESSION_EXPIRATION

    AppLogger().logger.info(f"[{datetime.datetime.now()}] Periodic session expiration task gets started by the loop")

    # Recommended way to set a periodic task with tornado.
    # See: https://buildmedia.readthedocs.org/media/pdf/tornado/latest/tornado.pdf, page 20.
    while True:
        AppLogger().logger.info(f"[{datetime.datetime.now()}] Periodic session expiration task begins database fetches")

        alive_sessions_query = select(Sessions.id, Sessions.closing_date, Sessions.expiration_date, Sessions.is_alive).\
            where(Sessions.is_alive == True)

        async with database_async_engine.connect() as database_async_connection:
            alive_sessions_coroutine = await database_async_connection.execute(alive_sessions_query)
            alive_sessions = alive_sessions_coroutine.all()

        # Collect the IDs of the sessions that will be expired.
        expired_sessions_ids = []
        for alive_session in alive_sessions:
            if alive_session.expiration_date <= datetime.datetime.now():
                print(alive_session.id, alive_session.is_alive, alive_session.expiration_date, datetime.datetime.now())
                expired_sessions_ids.append(alive_session.id)

        if expired_sessions_ids:
            expire_sessions_query = update(Sessions).where(Sessions.id.in_(expired_sessions_ids)).\
                values(is_alive=False)

            # Connection with context managers didn't update the rows, session + commit does the trick.
            async with AsynchronousSession() as session:
                result = await session.execute(expire_sessions_query)
                await session.commit()

            AppLogger().logger.info(f"[{datetime.datetime.now()}] Periodic session expiration task done, updated "
                                    f"{result.rowcount} sessions")
        else:
            AppLogger().logger.info(f"[{datetime.datetime.now()}] Periodic session expiration task done, no sessions "
                                    f"updated")

        await gen.sleep(task_config["task_delay"])
