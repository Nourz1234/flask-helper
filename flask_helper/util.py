import functools
import random
import string
from typing import Any, Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


class Lazy:
    def __init__(self, func):
        self._func = func

    @functools.cached_property
    def value(self):
        return self._func()


def set_msg(name: str, msg: str, category: str) -> None:
    from flask import session

    session[f"_{name}_m"] = msg
    session[f"_{name}_c"] = category


def pop_msg(name: str) -> tuple[str | None, str | None]:
    from flask import session

    msg = session.pop(f"_{name}_m", None)
    category = session.pop(f"_{name}_c", None)
    return msg, category


def request_cache(func: Callable[P, T]) -> Callable[P, T]:
    """
    Works like `lru_cache` but the cache is preserved only for the duration of the flask request.
    """
    from flask import g, has_app_context

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        if not has_app_context():
            return func(*args, **kwargs)

        property_name = f"_caching_func_{id(func)}"
        if hasattr(g, property_name):
            caching_func = getattr(g, property_name)
        else:
            caching_func = functools.lru_cache(func)
            setattr(g, property_name, caching_func)

        return caching_func(*args, **kwargs)

    return wrapper


def make_authorizer(auth_func: Callable[[], bool], description="Unauthorized."):
    """
    usage:
    ```python
    def auth_func():
        return request.headers.get("access-token") == ACCESS_TOKEN

    auth_required = make_authorizer(auth_func, "Invalid access token.")

    @app.route("/users")
    @auth_required
    def secure_endpoint():
        ...
    ```
    """
    from werkzeug.exceptions import Unauthorized as UnauthorizedError

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if not auth_func():
                raise UnauthorizedError(description=description)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def api_endpoint(func: Callable[P, T]) -> Callable[P, T]:
    """
    Marks the route as an API endpoint.
    API endpoints will return a JSON response on error instead of a HTML response.
    Should be used right after the `@app.route` decorator.

    example:
    ```
    @app.route('/users')
    @api_endpoint
    @login_required
    def users():
        ...
    ```

    Use `is_api_endpoint` to determine if the current request is on an API endpoint.
    """
    from flask import g

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        g.api_endpoint = True
        return func(*args, **kwargs)

    return wrapper


def is_api_endpoint() -> bool:
    from flask import g

    return g.get("api_endpoint", False)


def generate_token(length=50) -> str:
    """
    Generates a random string form numbers and upper and lower case letters.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def parse_bool(string: Any) -> bool:
    if isinstance(string, bool):
        return string
    if not isinstance(string, str):
        raise ValueError("Expecting a string to parse.")
    string = string.strip().lower()
    if string in ["true", "t", "yes", "y", "1"]:
        return True
    elif string in ["false", "f", "no", "n", "0"]:
        return False
    else:
        raise ValueError("String is not a boolean.")


def parse_bool_or_default(string: Any, default: bool = False) -> bool:
    try:
        return parse_bool(string)
    except ValueError:
        return default


def normalize_database_url(url: str) -> str:
    import re

    url = re.sub(r"^postgres\b", "postgresql", url)
    return url


def dict_keys_snake_case_to_kebab_case(dict: dict[str, Any]) -> dict[str, Any]:
    return {k.replace("_", "-"): v for k, v in dict.items()}
