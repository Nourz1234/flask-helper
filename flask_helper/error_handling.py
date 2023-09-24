from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .errors import ValidationError
from .util import is_api_endpoint


def init_error_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def _(err: HTTPException):
        if is_api_endpoint():
            return jsonify(status="error", description=err.description), err.code or 500
        else:
            return err

    @app.errorhandler(ValidationError)
    def _(err: ValidationError):
        if is_api_endpoint():
            return (
                jsonify(status="error", description=err.description, errors=err.errors),
                err.code or 400,
            )
        else:
            return err
