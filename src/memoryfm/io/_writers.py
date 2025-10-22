"""Module: _writers.py"""

from __future__ import annotations
import json
import io
from typing import TYPE_CHECKING
from memoryfm._typing import PathLike

if TYPE_CHECKING:
    from typing import IO


def _write_string(
    data: str,
    file: PathLike | IO[str] | None = None,
) -> str | None:
    """
    Write `dict` to JSON format.
    """
    if isinstance(file, PathLike):
        with open(file, "w") as fp:
            fp.write(data)
    elif isinstance(file, io.TextIOBase):
        file.write(data)
    else:
        return data
    return None


def _dict_to_json(
    data,
    file: PathLike | IO[str] | None = None,
) -> str | None:
    """
    Write `dict` to JSON format.
    """
    if isinstance(file, PathLike):
        with open(file, "w") as fp:
            json.dump(fp, data)
    elif isinstance(file, io.TextIOBase):
        json.dump(data, fp=file)
    else:
        return json.dumps(data)
    return None


def _dict_to_csv(
    data,
    file: PathLike | IO[str] | None = None,
) -> str | None:
    """
    Write `dict` to CSV format.
    """
    # if file is not None:
    #     file_like = _file_opener(file, "w")
    #     json.dump(data, file_like)
    #     file_like.close()
    # else:
    #     return data
    # return None
    return data
