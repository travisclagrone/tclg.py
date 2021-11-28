from collections.abc import Sequence
from typing import NoReturn, Optional


class exitable:
    """Context manager that provides a method to unexceptionally exit the block early.

    Multiple instances of this context manager may be nested while preserving the
    correct exiting semantics. I.e. calling `exit` on an outer exitable context from
    within an inner exitable context will correctly exit all the way through the outer
    exitable context (not just the closest enclosing exitable context). This may be used
    to emulate named breakable loops, for example.

    This context manager is NOT reentrant. This context manager is technically reusable,
    although reusing it is neither an intended use case nor advised.

    Example:
        >>> with exitable() as try_chain:
        ...     try:
        ...         from cytoolz import compose
        ...     except ModuleNotFoundError:
        ...         pass
        ...     else:
        ...         try_chain.exit()
        ...
        ...     try:
        ...         from toolz import compose
        ...     except ModuleNotFoundError:
        ...         pass
        ...     else:
        ...         try_chain.exit()
        ...
        ...     try:
        ...         from functoolz import compose
        ...     except ModuleNotFoundError:
        ...         pass
        ...     else:
        ...         try_chain.exit()
        ...
        ...     def compose(*funcs):
        ...         if not funcs:
        ...             return lambda x: x
        ...         def composed(*args, **kwargs):
        ...             it = reversed(funcs)
        ...             x = next(it)(*args)
        ...             for func in it:
        ...                 x = func(x)
        ...             return x
    """

    class __ContextExit(BaseException):
        pass

    def __init__(self):
        self.__exit_exc = self.__ContextExit()

    def __enter__(self) -> "exitable":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        return exc_value is None or exc_value is self.__exit_exc

    def exit(self) -> NoReturn:
        raise self.__exit_exc from None


class catch:
    """Context manager to catch (suppress and save) zero or more exceptions types.

    Example:
        >>> with catch(ModuleNotFoundError) as caught:
        ...     from cytoolz import compose
        ... if caught:
        ...     with catch(ModuleNotFoundError) as caught:
        ...         from toolz import compose
        ... if caught:
        ...     with catch(ModuleNotFoundError) as caught:
        ...         from functoolz import compose
        ... if caught:
        ...     def compose(*funcs):
        ...         if not funcs:
        ...             return lambda x: x
        ...         def composed(*args, **kwargs):
        ...             it = reversed(funcs)
        ...             x = next(it)(*args, **kwargs)
        ...             for func in it:
        ...                 x = func(x)
        ...             return x
    """

    types: Sequence[type]
    value: Optional[Exception]

    def __init__(self, *exc_types):
        assert all(isinstance(t, Exception) for t in exc_types)
        self.types = exc_types
        self.value = None

    def __enter__(self) -> "catch":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if exc_value is None:
            return True
        if any(isinstance(exc_value, t) for t in self.types):
            self.value = exc_value
            return True
        return False

    def __bool__(self) -> bool:
        return self.value is not None
