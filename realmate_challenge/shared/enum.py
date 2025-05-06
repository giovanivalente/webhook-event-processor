from enum import Enum


class BaseEnum(str, Enum):
    @classmethod
    def choices(cls):
        return ((item.value, item.name.title()) for item in cls)
