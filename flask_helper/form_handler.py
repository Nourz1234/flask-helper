from typing import Callable

from flask import request
from werkzeug.exceptions import BadRequest

from .forms import FlaskFormEx


class FormsHandler:
    handlers: list[tuple[Callable, type[FlaskFormEx]]]

    def __init__(self) -> None:
        self.handlers = []

    def form_handler(self, form_type: type[FlaskFormEx]):
        def wrapper(func):
            self.handlers.append((func, form_type))
            return func

        return wrapper

    def handle_request(self):
        for func, form_type in self.handlers:
            if (
                request.method == "GET"
                and request.args.get("form_name") == form_type.form_name
            ) or (request.form.get("form_name") == form_type.form_name):
                form = form_type()
                form.validate_or_raise()
                return func(form)
        raise BadRequest()
