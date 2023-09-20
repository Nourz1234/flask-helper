from typing import Callable

from flask import g, request
from werkzeug.exceptions import BadRequest

from .forms import FlaskFormEx


def form_handler(form_type: type[FlaskFormEx]):
    def decorator(func):
        if not hasattr(g, "_form_handlers"):
            g._form_handlers = []
        g._form_handlers.append((func, form_type))
        return func

    return decorator


def handle_form_submit():
    handlers: list[tuple[Callable, type[FlaskFormEx]]] = g.get("_form_handlers")
    handlers = handlers or []
    for func, form_type in handlers:
        if request.method == "GET":
            form_data = request.args
        else:
            form_data = request.form
        if (
            form_data.get("form_name") == form_type.form_name
            and request.method == form_type.form_method
        ):
            form = form_type()
            form.validate_or_raise()
            return func(form)
    raise BadRequest()
