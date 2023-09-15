from enum import Enum


class Environment(str, Enum):
    Production = "production"
    Development = "development"
