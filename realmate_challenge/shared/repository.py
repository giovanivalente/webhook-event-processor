from abc import ABC
from typing import Generic, TypeVar

from django.core.exceptions import ObjectDoesNotExist

TModel = TypeVar('TModel')


class BaseRepository(ABC, Generic[TModel]):
    model: type[TModel]

    def create(self, **kwargs) -> TModel:
        return self.model.objects.create(**kwargs)

    def safe_get(self, **kwargs) -> TModel | None:
        try:
            return self.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def update(self, obj, /, **kwargs) -> TModel:
        has_changes = False

        for key, value in kwargs.items():
            if not hasattr(obj, key):
                raise AttributeError(f"{obj.__class__.__name__} has no attribute '{key}'")

            current_value = getattr(obj, key)
            if value != current_value:
                setattr(obj, key, value)
                has_changes = True

        if has_changes:
            obj.save()

        return obj
