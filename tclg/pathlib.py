# TODO LATER consider renaming `tclg.pathlib` to `tclg.fsutil` and import it as `fs`
import os
import shutil as sh

from collections.abc import Iterator
from os import PathLike
from pathlib import Path
from typing import Optional, Union


__all__ = []

def export(named):
    assert named.__name__ is not None
    __all__.append(named.__name__)
    return named


# region Directories

cwd = export(Path.cwd)
home = export(Path.home)


@export
def chdir(path: Union[PathLike, str] = None, /) -> Path:
    path = Path.home() if path is None else Path(path)
    os.chdir(path)
    return path.resolve()


@export
def lsdir(path: Union[PathLike, str] = None, /) -> list[Path]:
    path = Path() if path is None else Path(path)
    return list(path.iterdir())


# TODO def lsdirs(path: Union[PathLike, str] = None, /) -> Iterator[Path]
# (recursive)


@export
def mkdir(
    path: Union[PathLike, str],
    /,
    mode: int = None,
    *,
    unlink: bool = False,
    rmtree: bool = False,
) -> Path:
    path = Path(path)
    if unlink and (path.is_file() or path.is_symlink()):
        path.unlink()
    elif rmtree and path.is_dir():
        sh.rmtree(path)

    kwargs = {"parents": True, "exist_ok": True}
    if mode is not None:
        kwargs["mode"] = mode
    path.mkdir(**kwargs)
    return path


# TODO def mkdirs(...)
# REFACTOR separate mkdir(...) into mkdir (no init parents) and mkdirs (init parents)


# TODO def mvdir(...)
# (like mkdir, not mkdirs)


# TODO def mvdirs(...)
# (like mkdirs + rmdirs)


@export
def rmdir(path: Union[PathLike, str], /) -> Optional[Path]:
    path = Path(path)
    if path.exists():
        path.rmdir()
        return path


@export
def rmdirs(path: Union[PathLike, str], /) -> list[Path]:
    removed = []
    path = Path(path)
    if path.exists():
        path.rmdir()
        removed.append(path)
    for parent in path.parents:
        if not parent.exists():
            continue
        try:
            parent.rmdir()
        except OSError:
            break
        else:
            removed.append(parent)
    return removed

# endregion


# region Trees

# TODO def cptree(...)


# TODO def mktree(...)
# (create a file(s) and init parent directories if needed)


# TODO def mvtree(...)


# TODO def rmtree(...)
# (remove directory and all of its children--including files--recursively)

# endregion


# region Files

# TODO def cp(file, ...)
# (requires the destination to not already exist unless an explicit flag is passed)


# TODO def mk(file, ...)
# (similar to `pathlib.Path.touch`, but perhaps including an option to force re-create)


# TODO def mv(file, ...)
# (equivalent to `Path.rename`, but with a flag param to be `Path.replace`)


@export
def rm(path: Union[PathLike, str], /, missing_ok: bool = True) -> None:
    path = Path(path)
    path.unlink(missing_ok=missing_ok)


# TODO def which(cmd, ...) -> Path

# endregion


# region Links

# TODO hardlink(...)
# (see `pathlib.Path.hardlink_to`)


# TODO symlink(...)
# (see `pathlib.Path.symlink_to`)


# TODO readlink(...)
# (see `pathlib.Path.readlink`)


# TODO unlink(...)
# (see `pathlib.Path.unlink`)

# endregion


# region Globs

@export
def glob(pattern: str, /, root_dir: Union[PathLike, str] = None) -> list[Path]:
    root_dir = Path() if root_dir is None else Path(root_dir)
    return list(root_dir.glob(pattern))


@export
def rglob(pattern: str, /, root_dir: Union[PathLike, str] = None) -> Iterator[Path]:
    root_dir = Path() if root_dir is None else Path(root_dir)
    return root_dir.rglob(pattern)

# endregion
