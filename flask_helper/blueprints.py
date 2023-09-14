from typing import Any, Callable

from flask import Blueprint, Flask, blueprints


class Blueprint(blueprints.Blueprint):
    def make_setup_state(
        self, app: Flask, options: dict, first_registration: bool = False
    ) -> blueprints.BlueprintSetupState:
        return BlueprintSetupState(self, app, options, first_registration)


class BlueprintSetupState(blueprints.BlueprintSetupState):
    def __init__(
        self, blueprint: Blueprint, app: Flask, options: Any, first_registration: bool
    ) -> None:
        self.host = options.pop("host", None)
        if (
            self.host is not None
            and "PORT" in app.config
            and app.config["PORT"] != 80
        ):
            self.host = f"{self.host}:{app.config['PORT']}"
        super().__init__(blueprint, app, options, first_registration)

    def add_url_rule(
        self,
        rule: str,
        endpoint: str | None = None,
        view_func: Callable | None = None,
        **options: Any,
    ) -> None:
        options.update(host=self.host)
        return super().add_url_rule(rule, endpoint, view_func, **options)
