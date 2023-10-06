import functools
from typing import Callable, Concatenate, ParamSpec, TypeVar

from flask import g, request
from flask import typing as ft
from werkzeug.exceptions import BadRequest

from .forms import APIForm, FlaskFormEx

P = ParamSpec("P")
T_FlaskForm = TypeVar("T_FlaskForm", bound=FlaskFormEx)
T_APIForm = TypeVar("T_APIForm", bound=APIForm)


def form_handler(form_type: type[T_FlaskForm]):
    if not issubclass(form_type, FlaskFormEx):
        raise TypeError(f"Expecting a subclass of {FlaskFormEx.__name__}")

    def decorator(func: Callable[[T_FlaskForm], ft.ResponseReturnValue]):
        if not hasattr(g, "_form_handlers"):
            g._form_handlers = []
        g._form_handlers.append((func, form_type))
        return func

    return decorator


def handle_form_submit():
    handlers: list[
        tuple[Callable[[FlaskFormEx], ft.ResponseReturnValue], type[FlaskFormEx]]
    ] = g.get("_form_handlers", [])
    if not handlers:
        raise RuntimeError("No form handlers where defined for the current request.")
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


def api_endpoint_form(form_type: type[T_APIForm]):
    if not issubclass(form_type, APIForm):
        raise TypeError(f"Expecting a subclass of {APIForm.__name__}")

    def decorator(func: Callable[Concatenate[T_APIForm, P], ft.ResponseReturnValue]):
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> ft.ResponseReturnValue:
            form = form_type()
            form.validate_or_raise()
            return func(form, *args, **kwargs)

        return wrapper

    return decorator
