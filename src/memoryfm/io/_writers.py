"""Module: _writers.py
"""

from __future__ import annotations
import json
from typing import TYPE_CHECKING
from memoryfm.util._file_handler import _file_opener

if TYPE_CHECKING:
    from typing import IO
    from memoryfm._typing import PathLike


def _write_string(
    data: str,
    file: PathLike | IO[str] | None = None,
) ->None:
    """
    Write `dict` to JSON format.
    """
    if file is not None:
        file_like = _file_opener(file, "w")
        file_like.write(data)
        file_like.close()
    else:
        return data
    return None

def _dict_to_json(
    data,
    file: PathLike | IO[str] | None = None,
) ->str | None:
    """
    Write `dict` to JSON format.
    """
    if file is not None:
        file_like = _file_opener(file, "w")
        json.dump(data, file_like)
        file_like.close()
    else:
        return json.dumps(data)
    return None

def _dict_to_csv(
    data,
    file: PathLike | IO[str] | None = None,
) ->str | None:
    """
    Write `dict` to CSV format.
    """
    if file is not None:
        file_like = _file_opener(file, "w")
        json.dump(data, file_like)
        file_like.close()
    else:
        return data
    return None
