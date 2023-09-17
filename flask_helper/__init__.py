from flask import Flask

from . import blueprints
from .error_handling import init_error_handlers # pyright: ignore

__version__ = "1.14"

def init_template_globals(app: Flask):
    from .util import pop_msg

    app.add_template_global(pop_msg)

    app.add_template_filter(zip)
    app.add_template_filter(enumerate)


blueprint = blueprints.Blueprint(
    "flask_helper_blueprint",
    __name__,
    static_folder="assets",
    static_url_path="/assets/helper",
    template_folder="templates",
)
