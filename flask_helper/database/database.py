import functools
from contextvars import ContextVar
from typing import Callable, ParamSpec, TypeVar

import sqlalchemy
from sqlalchemy.orm import Session, scoped_session, sessionmaker

T = TypeVar("T")
P = ParamSpec("P")


class Database:
    engine: sqlalchemy.Engine | None = None
    _session: scoped_session[Session] | None = None
    _context_entered: ContextVar[int] = ContextVar("_context_entered", default=0)

    def init(self, url, session_options):
        if self._session:
            raise RuntimeError("Database is already initialized.")

        self.engine = sqlalchemy.create_engine(url)
        self._session = scoped_session(sessionmaker(bind=self.engine, **session_options))

    @property
    def session(self):
        if not self._session:
            raise RuntimeError(
                "Accessing database session before initialization. "
                "Did you forget to call '.init()'?"
            )
        if not self.context_entered:
            raise RuntimeError("Accessing database session out of database context.")
        return self._session

    @property
    def context_entered(self):
        return self._context_entered.get() > 0

    def context(self, func: Callable[P, T]) -> Callable[P, T]:
        if not self._session:
            raise RuntimeError(
                "Declaring a database context before initialization. "
                "Did you forget to call '.init()'?"
            )

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                self._context_entered.set(self._context_entered.get() + 1)
                return func(*args, **kwargs)
            finally:
                level = self._context_entered.get() - 1
                self._context_entered.set(level)
                if level == 0:
                    self.session.remove()

        return wrapper
