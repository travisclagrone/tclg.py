from typing import Protocol, runtime_checkable


@runtime_checkable
class Exitable(Protocol):
    def exit(self):
        ...


@runtime_checkable
class SupportsDelAttr(Protocol):
    def __delattr__(self, key):
        ...


@runtime_checkable
class SupportsDelItem(Protocol):
    def __delitem__(self, key):
        ...


@runtime_checkable
class SupportsGetAttr(Protocol):
    def __getattr__(self, name):
        ...


@runtime_checkable
class SupportsGetAttribute(Protocol):
    def __getattribute__(self, name):
        ...


@runtime_checkable
class SupportsGetItem(Protocol):
    def __getitem__(self, key):
        ...


@runtime_checkable
class SupportsSetAttr(Protocol):
    def __setattr__(self, name, value):
        ...


@runtime_checkable
class SupportsSetItem(Protocol):
    def __setitem__(self, key, value):
        ...
