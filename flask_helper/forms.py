import flask_wtf
from flask_wtf.file import FileAllowed, FileField
from werkzeug.exceptions import Forbidden
from wtforms import HiddenField
from wtforms.fields.core import UnboundField
from wtforms.form import FormMeta

from .const import FormEncodingType
from .errors import ValidationError


class FormMetaClass(FormMeta):
    def __new__(cls, name, bases, attr):
        # detect if there is a file field and update enctype
        file_fields = [
            val
            for val in attr.values()
            if isinstance(val, UnboundField) and val.field_class is FileField
        ]
        if file_fields:
            attr["form_enctype"] = FormEncodingType.MULTIPART.value

        # detect "FileAllowed" validator and use it to populate "accept" attribute
        for file_field in file_fields:
            validators = file_field.kwargs.get("validators")
            if not validators:
                continue

            file_allowed_validators = [
                validator
                for validator in validators
                if isinstance(validator, FileAllowed)
            ]
            if not file_allowed_validators:
                continue

            render_kw = file_field.kwargs.get("render_kw", {})
            if "accept" not in render_kw:
                upload_set = file_allowed_validators[0].upload_set
                accept = ",".join([f".{ext}" for ext in upload_set])
                render_kw["accept"] = accept
                file_field.kwargs["render_kw"] = render_kw

        return super().__new__(cls, name, bases, attr)


class FlaskFormEx(flask_wtf.FlaskForm, metaclass=FormMetaClass):
    form_name: str = None
    form_method: str = "POST"
    form_enctype: FormEncodingType = FormEncodingType.URL_ENCODED.value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_name_field.data = self.form_name
        self.form_method_field.data = self.form_method.lower()

    form_name_field = HiddenField(name="form_name")
    form_method_field = HiddenField(name="form_method")

    def validate_or_raise(self):
        if not self.validate():
            if "csrf_token" in self.errors:
                raise Forbidden(self.errors["csrf_token"][0])
            raise ValidationError(self.errors)
