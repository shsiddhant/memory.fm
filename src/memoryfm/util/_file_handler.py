"""Module: memoryfm.util._readers"""

from __future__ import annotations
import io
from typing import TYPE_CHECKING
from memoryfm._typing import PathLike

if TYPE_CHECKING:
    from typing import IO

def _file_opener(
    file: PathLike | IO[str] = None,
    mode: str = "r"
) ->IO[str] | None:
    """Return file-like object from PathLike or file-like object
    """
    if file is None:
        raise TypeError("No Path or file specified")
    if isinstance(file, io.TextIOBase):
        return file
    elif isinstance(file, PathLike):
        file_like = open(file, mode)
        return file_like
    else:
        raise TypeError("Expected PathLike or file-like object")
