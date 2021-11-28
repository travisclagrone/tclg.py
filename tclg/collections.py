from collections.abc import Iterator, Mapping, MutableMapping, Sequence
from typing import Any, Generic, Optional, TypeVar


__all__ = []
__dir__ = lambda: __all__


def export(definition):
    __all__.append(definition.__name__)
    return definition


def attr_error(name: str, obj: Any) -> AttributeError:
    msg = f"'{type(obj).__name__}' object has no attribute '{name}'"
    return AttributeError(msg, name=name, obj=obj)


def is_public(name: str) -> bool:
    return not name.startswith("_")


V = TypeVar("V")


@export
class AttrsItemsView(Generic[V]):
    """View of a collection of items (i.e. a `Mapping`) as an `object` of attributes."""

    def __init__(self, data: Mapping[str, V]):
        if not isinstance(data, Mapping):
            raise TypeError(f"Expected data to be a Mapping, not a {type(data)}")
        self._data = data

    def __dir__(self) -> Sequence[str]:
        return tuple(filter(is_public, self._data.keys()))

    def __getattr__(self, name: str) -> V:
        if not is_public(name):
            raise attr_error(name, self)
        try:
            return self._data[name]
        except KeyError as exc:
            raise attr_error(name, self) from exc

    __setattr__ = None
    __delattr__ = None


@export
class MutableAttrsItemsView(AttrsItemsView):
    """View of a mutable collection of items (i.e. a `MutableMapping`) as an `object` of attributes."""

    def __init__(self, data: MutableMapping[str, V]):
        if not isinstance(data, MutableMapping):
            raise TypeError(f"Expected data to be a MutableMapping, not a {type(data)}")
        self._data = data

    def __setattr__(self, name: str, value: V) -> None:
        if not is_public(name):
            raise attr_error(name, self)
        try:
            self._data[name] = value
        except KeyError as exc:
            raise attr_error(name, self) from exc

    def __delattr__(self, name: str) -> None:
        if not is_public(name):
            raise attr_error(name, self)
        try:
            del self._data[name]
        except KeyError as exc:
            raise attr_error(name, self) from exc


@export
class ItemsAttrsView(Mapping[str, Optional[Any]]):
    """View of a structure of attributes (i.e. an `object`) as a `Mapping` of items."""

    def __init__(self, obj: Any):
        if obj is None:
            raise TypeError(f"Expected obj to be an object, not None")
        self._obj = obj

    def __getitem__(self, key: str) -> Optional[Any]:
        if not is_public(key):
            raise KeyError(key)
        try:
            return getattr(self._obj, key)
        except AttributeError as exc:
            raise KeyError(key) from exc

    def __iter__(self) -> Iterator:
        return filter(is_public, dir(self._obj))

    def __len__(self) -> int:
        return sum(map(is_public, dir(self._obj)))


@export
class MutableItemsAttrsView(ItemsAttrsView):
    """View of a mutable structure of attributes (i.e. an `object`) as a `MutableMapping` of items."""

    def __init__(self, obj: Any):
        if not hasattr(obj, "__setattr__"):
            raise TypeError(f"Expected obj's attributes to be settable")
        if not hasattr(obj, "__delattr__"):
            raise TypeError(f"Expected obj's attributes to be deletable")
        super().__init__(obj)

    def __setitem__(self, key: str, value: Optional[Any]) -> None:
        if not is_public(key):
            raise KeyError(key)
        try:
            setattr(self._obj, key, value)
        except AttributeError as exc:
            raise KeyError(key) from exc

    def __delitem__(self, key: str) -> None:
        if not is_public(key):
            raise KeyError(key)
        try:
            delattr(self._obj, key)
        except AttributeError as exc:
            raise KeyError(key) from exc


__all__ = tuple(__all__)
