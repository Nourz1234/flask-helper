import functools
import random
import string
from typing import Any


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


def request_cache(func):
    from flask import g

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        property_name = f"_{func.__name__}_return"
        if hasattr(g, property_name):
            value = getattr(g, property_name)
        else:
            value = func(*args, **kwargs)
            setattr(g, property_name, value)

        return value

    return wrapper


def api_endpoint(func):
    from flask import g

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        g.api_endpoint = True
        return func(*args, **kwargs)

    return wrapper


def is_api_endpoint() -> bool:
    from flask import g

    return g.get("api_endpoint", False)


def generate_token(length=50) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def parse_bool(x: Any) -> bool:
    if isinstance(x, bool):
        return x
    if not isinstance(x, str):
        raise ValueError("Expecting a string to parse")
    x = x.strip().lower()
    if x in ["true", "t", "yes", "y", "1"]:
        return True
    elif x in ["false", "f", "no", "n", "0"]:
        return False
    else:
        raise ValueError("String is not a boolean")


def parse_bool_or_default(string: Any, default: bool = False) -> bool:
    try:
        return parse_bool(string)
    except ValueError:
        return default


def normalize_database_url(url: str):
    import re

    url = re.sub(r"^postgres\b", "postgresql", url)
    return url


def dict_keys_snake_case_to_kebab_case(dict: dict[str, Any]):
    return {k.replace("_", "-"): v for k, v in dict.items()}
