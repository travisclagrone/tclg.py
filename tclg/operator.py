from typing import Any, Optional

from tclg.typing import (
    SupportsDelAttr,
    SupportsDelItem,
    SupportsSetAttr,
    SupportsSetItem,
)


class attrdeleter:
    """Return a callable object that deletes the named attribute of its operand.

    Args:
        name (str): name of the attribute to delete

    Returns:
        Callable[[SupportsDelAttr], None]: callable that mutates its attribute-supporting argument and returns nothing
    """

    def __init__(self, name: str):
        self._name = name

    def __call__(self, obj: SupportsDelAttr) -> None:
        delattr(obj, self._name)


class attrsetter:
    """Return a callable object that sets the named attribute of its operand to the given value.

    Args:
        name (str): name of the attribute to set
        value (Optional[Any]): value to which to set the attribute

    Returns:
        Callable[[SupportsSetAttr], None]: callable that mutates its attribute-supporting argument and returns nothing
    """

    def __init__(self, name: str, value: Optional[Any]) -> None:
        self._name = name
        self._value = value

    def __call__(self, obj: SupportsSetAttr) -> None:
        setattr(obj, self._name, self._value)


class itemdeleter:
    """Return a callable object that deletes the keyed item of its operand.

    Args:
        key (Optional[Any]): key of the item to delete

    Returns:
        Callable[[SupportsDelItem], None]: callable that mutates its item-supporting argument and returns nothing
    """

    def __init__(self, key: Optional[Any]):
        self._key = key

    def __call__(self, obj: SupportsDelItem) -> None:
        del obj[self._key]


class itemsetter:
    """Return a callable object that sets the keyed item to the given value from its operand.

    Args:
        name (Optional[Any]): key of the item to set
        value (Optional[Any]): value to which to set the item

    Returns:
        Callable[[SupportsSetItem], None]: callable that mutates its item-supporting argument and returns nothing
    """

    def __init__(self, key: Optional[Any], value: Optional[Any]) -> None:
        self._key = key
        self._value = value

    def __call__(self, obj: SupportsSetItem) -> None:
        obj[self._key] = self._value
