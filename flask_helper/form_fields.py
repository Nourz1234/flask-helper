from wtforms import Field
from wtforms.widgets import TextInput


class StringListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return ", ".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist: list[str]):
        if valuelist:
            try:
                values = [value.strip() for value in valuelist[0].split(",")]
                self.data = [value for value in values if value]
            except (ValueError, TypeError) as exc:
                raise ValueError(self.gettext("Not a valid comma-separated values.")) from exc
        else:
            self.data: list[str] = []


class IntegerListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return ", ".join(map(str, self.data))
        else:
            return ""

    def process_formdata(self, valuelist: list[str]):
        if valuelist:
            try:
                values = [value.strip() for value in valuelist[0].split(",")]
                self.data = [int(value) for value in values if value]
            except (ValueError, TypeError) as exc:
                raise ValueError(self.gettext("Not a valid comma-separated integers.")) from exc
        else:
            self.data: list[int] = []
