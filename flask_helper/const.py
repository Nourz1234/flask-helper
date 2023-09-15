from enum import Enum


class Environment(str, Enum):
    Production = "production"
    Development = "development"


class FormEncodingType(str, Enum):
    URL_ENCODED = "application/x-www-form-urlencoded"
    MULTIPART = "multipart/form-data"
