from contextvars import ContextVar
from typing import Any, Callable

from flask import Blueprint, Flask, blueprints
from flask.app import Flask

_host: ContextVar[str | None] = ContextVar("_host", default=None)
_host_set: ContextVar[bool] = ContextVar("_host_set", default=False)


class Blueprint(blueprints.Blueprint):
    def register(self, app: Flask, options: dict) -> None:
        if "host" in options and not _host_set.get():
            _host.set(options.get("host"))
            _host_set.set(True)

            try:
                return super().register(app, options)
            finally:
                _host.set(None)
                _host_set.set(False)
        else:
            return super().register(app, options)

    def make_setup_state(
        self, app: Flask, options: dict, first_registration: bool = False
    ) -> blueprints.BlueprintSetupState:
        return BlueprintSetupState(self, app, options, first_registration)


class BlueprintSetupState(blueprints.BlueprintSetupState):
    def __init__(
        self, blueprint: Blueprint, app: Flask, options: Any, first_registration: bool
    ) -> None:
        super().__init__(blueprint, app, options, first_registration)

        self.host = _host.get()
        if self.host is not None and "PORT" in app.config and app.config["PORT"] != 80:
            self.host = f"{self.host}:{app.config['PORT']}"

    def add_url_rule(
        self,
        rule: str,
        endpoint: str | None = None,
        view_func: Callable | None = None,
        **options: Any,
    ) -> None:
        if self.host is not None:
            options.update(host=self.host)
        return super().add_url_rule(rule, endpoint, view_func, **options)
