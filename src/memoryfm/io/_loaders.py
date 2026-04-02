from __future__ import annotations
from typing import TYPE_CHECKING
import io
import json
from pathlib import Path
from memoryfm.errors import ParseError


if TYPE_CHECKING:
    from typing import (
        IO,
    )


def load_json(file: str | Path | IO[str]) -> dict | None:
    """
    Read JSON file and return a dictionary.

    Parameters
    ----------
    file: PathLike object such as open( or file/file-like object

    """
    data = None
    try:
        if isinstance(file, io.TextIOBase):
            data = json.load(file)
        elif isinstance(file, (str, Path)):
            with open(file) as fp:
                data = json.load(fp)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as e:
        raise ParseError(file, f"{e.msg} at line {e.lineno} column {e.colno}")
    return data
