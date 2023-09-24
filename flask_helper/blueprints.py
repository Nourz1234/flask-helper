from typing import Any, Callable

from flask import Flask, blueprints


class Blueprint(blueprints.Blueprint):
    def register(self, app: Flask, options: dict) -> None:
        prev_host = getattr(app, "_blueprint_host", None)
        setattr(app, "_blueprint_host", options.get("host"))

        try:
            return super().register(app, options)
        finally:
            setattr(app, "_blueprint_host", prev_host)

    def make_setup_state(
        self, app: Flask, options: dict, first_registration: bool = False
    ) -> blueprints.BlueprintSetupState:
        return BlueprintSetupState(self, app, options, first_registration)


class BlueprintSetupState(blueprints.BlueprintSetupState):
    def __init__(
        self, blueprint: Blueprint, app: Flask, options: Any, first_registration: bool
    ) -> None:
        super().__init__(blueprint, app, options, first_registration)

        self.host: str | None = getattr(app, "_blueprint_host")
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
