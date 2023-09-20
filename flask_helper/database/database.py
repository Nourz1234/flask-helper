import functools
from contextvars import ContextVar

import sqlalchemy
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class Database:
    engine: sqlalchemy.Engine = None
    _session: scoped_session[Session] = None
    _context_entered: ContextVar[int] = ContextVar("_context_entered", default=0)

    def init(self, url, session_options):
        if self.engine:
            raise Exception("Database is already initialized.")

        self.engine = sqlalchemy.create_engine(url)
        self._session = scoped_session(
            sessionmaker(bind=self.engine, **session_options)
        )

    @property
    def session(self):
        if not self.engine:
            raise RuntimeError("Must call 'init()' on the database first.")
        if not self.context_entered:
            raise RuntimeError(
                "Can't access the session outside of the database context."
            )
        return self._session

    @property
    def context_entered(self):
        return self._context_entered.get() > 0

    def context(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self._context_entered.set(self._context_entered.get() + 1)
                return func(*args, **kwargs)
            finally:
                level = self._context_entered.get() - 1
                self._context_entered.set(level)
                if level == 0:
                    self._session.remove()

        return wrapper
