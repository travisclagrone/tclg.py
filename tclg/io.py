from collections.abc import Iterable
from io import BufferedIOBase, BytesIO, IOBase, RawIOBase, StringIO, TextIOBase
from os import PathLike
from pathlib import Path
from typing import Union, overload


__all__ = []
__dir__ = lambda: __all__

def _export(definition):
    assert definition.__name__ is not None
    __all__.append(definition.__name__)
    return definition


@overload
def read(file: Union[BufferedIOBase, RawIOBase], /) -> bytes:
    ...

@overload
def read(file: Union[TextIOBase, PathLike, str], /) -> str:
    ...

@_export
def read(file, /):
    match file:
        case RawIOBase():
            return file.readall()
        case BufferedIOBase() | TextIOBase():
            return file.read()
        case BytesIO() | StringIO():
            return file.getvalue()
        case Path():
            return file.read_text()
        case _:
            return Path(file).read_text()


@overload
def write(file: Union[BufferedIOBase, RawIOBase], value: bytes, /, *, flush: bool=True, close: bool=False) -> int:
    ...

@overload
def write(file: Union[PathLike, str], value: bytes, /) -> int:
    ...

@overload
def write(file: TextIOBase, value: str, /, *, flush: bool=True, close: bool=False) -> int:
    ...

@overload
def write(file: Union[PathLike, str], value: str, /) -> int:
    ...

@_export
def write(file, value, /, *, flush=True, close=False):
    if isinstance(file, IOBase):
        try:
            count = file.write(value)
            if flush:
                file.flush()
            return count
        finally:
            if close:
                file.close()

    if not isinstance(file, Path):
        file = Path(file)
    match value:
        case bytes():
            return file.write_bytes(value)
        case str():
            return file.write_str(value)
        case _:
            raise TypeError(f"Expected type of value to be str or bytes, but found that it was {type(value)}")


@overload
def append(file: Union[BufferedIOBase, RawIOBase], value: bytes, /, *, flush: bool=True, close: bool=False) -> int:
    ...

@overload
def append(file: Union[PathLike, str], value: bytes, /) -> int:
    ...

@overload
def append(file: TextIOBase, value: str, /, *, flush: bool=True, close: bool=False) -> int:
    ...

@overload
def append(file: Union[PathLike, str], value: str, /) -> int:
    ...

@_export
def append(file, value, /, *, flush=True, close=False):
    if isinstance(file, IOBase):
        try:
            count = file.write(value)
            if flush:
                file.flush()
            return count
        finally:
            if close:
                file.close()

    match value:
        case bytes():
            with open(file, mode='ab') as f:
                return f.write(value)
        case str():
            with open(file, mode='at') as f:
                return f.write(value)
        case _:
            raise TypeError(f"Expected type of value to be str or bytes, but found that it was {type(value)}")


@overload
def readlines(file: Union[BufferedIOBase, RawIOBase], /) -> list[bytes]:
    ...

@overload
def readlines(file: Union[TextIOBase, PathLike, str], /) -> list[str]:
    ...

@_export
def readlines(file, /):
    if isinstance(file, IOBase):
        return file.readlines()

    with open(file, mode="rt") as f:
        return f.readlines()


@overload
def writelines(file: Union[BufferedIOBase, RawIOBase], lines: Iterable[bytes], /, *, flush: bool=True, close: bool=False) -> None:
    ...

@overload
def writelines(file: Union[PathLike, str], lines: Iterable[bytes], /) -> None:
    ...

@overload
def writelines(file: TextIOBase, lines: Iterable[str], /, *, flush: bool=True, close: bool=False) -> None:
    ...

@overload
def writelines(file: Union[PathLike, str], lines: Iterable[str], /) -> None:
    ...

@_export
def writelines(file, lines, /, *, flush=True, close=False):
    if isinstance(file, IOBase):
        try:
            file.writelines(lines)
            if flush:
                file.flush()
            return
        finally:
            if close:
                file.close()

    with open(file, mode='wt') as f:
        f.writelines(lines)


@overload
def appendlines(file: Union[BufferedIOBase, RawIOBase], lines: Iterable[bytes], /, *, flush: bool=True, close: bool=False) -> None:
    ...

@overload
def appendlines(file: Union[PathLike, str], lines: Iterable[bytes], /) -> None:
    ...

@overload
def appendlines(file: TextIOBase, lines: Iterable[str], /, *, flush: bool=True, close: bool=False) -> None:
    ...

@overload
def appendlines(file: Union[PathLike, str], lines: Iterable[str], /) -> None:
    ...

@_export
def appendlines(file, lines, /, *, flush=True, close=False):
    if isinstance(file, IOBase):
        try:
            file.writelines(lines)
            if flush:
                file.flush()
            return
        finally:
            if close:
                file.close()

    with open(file, mode='at') as f:
        f.writelines(lines)
