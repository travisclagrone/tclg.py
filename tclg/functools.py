from collections.abc import Callable
from types import FunctionType


def do(func, arg):
    func(arg)
    return arg


def owner(cls: type) -> Callable[[FunctionType], None]:
    """Set the decorated function as an eponymous attribute of `cls`.

    Args:
        cls (type): the ``__dict__``-enabled class to own the decorated function

    Returns:
        Callable[[FunctionType], None]: the decorated function is not returned afterwards
    """

    def setowner(func: FunctionType) -> None:
        name = func.__name__
        setattr(cls, name, func)

    return setowner
