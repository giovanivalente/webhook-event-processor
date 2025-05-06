from enum import Enum


class BaseEnum(str, Enum):
    @classmethod
    def choices(cls):
        return tuple((item.value, item.name.title()) for item in cls)
