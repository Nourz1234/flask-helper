import functools
from typing import Callable, ParamSpec, TypeVar

from flask import g, request
from werkzeug.exceptions import BadRequest

from .forms import APIForm, FlaskFormEx

T = TypeVar("T")
P = ParamSpec("P")
T_FlaskForm = TypeVar("T_FlaskForm", bound=FlaskFormEx)
T_APIForm = TypeVar("T_APIForm", bound=APIForm)


def form_handler(form_type: type[T_FlaskForm]):
    if not issubclass(form_type, FlaskFormEx):
        raise TypeError(f"Expecting a subclass of {FlaskFormEx.__name__}")

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        if not hasattr(g, "_form_handlers"):
            g._form_handlers = []
        g._form_handlers.append((func, form_type))
        return func

    return decorator


def handle_form_submit():
    handlers: list[tuple[Callable, type[FlaskFormEx]]] = g.get("_form_handlers", [])
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

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            form = form_type()
            form.validate_or_raise()
            kwargs.update(form=form)
            return func(*args, **kwargs)

        return wrapper

    return decorator
