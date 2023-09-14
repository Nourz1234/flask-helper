from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .errors import ValidationError
from .util import is_api_endpoint


def init_error_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def error_handler(err: HTTPException):
        if is_api_endpoint():
            return jsonify(status="error", description=err.description), err.code
        else:
            return err

    @app.errorhandler(ValidationError)
    def error_handler(err: ValidationError):
        if is_api_endpoint():
            return (
                jsonify(status="error", description=err.description, errors=err.errors),
                err.code,
            )
        else:
            return err
