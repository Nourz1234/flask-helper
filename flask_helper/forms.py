from flask_wtf import FlaskForm
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
            raise ValidationError(self.errors)
