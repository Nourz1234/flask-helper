from flask_wtf import FlaskForm
from werkzeug.exceptions import Forbidden
from wtforms import HiddenField

from .errors import ValidationError


class FlaskFormEx(FlaskForm):
    form_name: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_name_.data = self.form_name

    form_name_ = HiddenField(name="form_name")

    def validate_or_raise(self):
        if not self.validate():
            if "csrf_token" in self.errors:
                raise Forbidden(self.errors["csrf_token"])
            raise ValidationError(self.errors)
