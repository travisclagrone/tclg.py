from typing import Protocol, runtime_checkable


__all__ = []
__dir__ = lambda: __all__

def _export(definition):
    assert definition.__name__ is not None
    __all__.append(definition.__name__)
    return definition


@runtime_checkable
@_export
class Exitable(Protocol):
    def exit(self):
        ...


@runtime_checkable
@_export
class SupportsDelAttr(Protocol):
    def __delattr__(self, key):
        ...


@runtime_checkable
@_export
class SupportsDelItem(Protocol):
    def __delitem__(self, key):
        ...


@runtime_checkable
@_export
class SupportsGetAttr(Protocol):
    def __getattr__(self, name):
        ...


@runtime_checkable
@_export
class SupportsGetAttribute(Protocol):
    def __getattribute__(self, name):
        ...


@runtime_checkable
@_export
class SupportsGetItem(Protocol):
    def __getitem__(self, key):
        ...


@runtime_checkable
@_export
class SupportsSetAttr(Protocol):
    def __setattr__(self, name, value):
        ...


@runtime_checkable
@_export
class SupportsSetItem(Protocol):
    def __setitem__(self, key, value):
        ...
