import os
from typing import Callable

import dotenv
from flask import Flask

from .util import parse_bool


def run(app_factory: Callable[[], Flask]):
    dotenv.load_dotenv()
    app = app_factory()
    app.run(
        port=app.config.get("PORT", 5000),
        use_reloader=parse_bool(os.environ.get("USE_RELOADER", "True")),
    )
