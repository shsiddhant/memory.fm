"""Module: memoryfm.utils.loaders
Handle JSON file inputs, possible errors, and parsing of JSON data into
a dictionary or pandas DataFrame for further processing depending on the JSON source.
"""

from __future__ import annotations
import json
import io
import pandas as pd
from csv import reader
from typing import TYPE_CHECKING
from memoryfm.errors import ParseError
from memoryfm._typing import PathLike


if TYPE_CHECKING:
    from typing import (
        IO,
        Any,
    )


def load_json(file: PathLike | IO[str] | None = None) -> Any:
    """
    Read JSON file and return a dictionary.

    Parameters
    ----------
    file: PathLike object such as open( or file/file-like object

    """
    try:
        if isinstance(file, io.TextIOBase):
            data = json.load(file)
        elif isinstance(file, PathLike):
            with open(file) as fp:
                data = json.load(fp)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as e:
        raise ParseError(file, f"{e.msg} at line {e.lineno} column {e.colno}")
    return data


def load_csv(file: PathLike | IO[str] | None = None) -> Any:
    """ """
    if isinstance(file, io.TextIOBase):
        fp = file
    elif isinstance(file, PathLike):
        fp = open(file, "r")
    else:
        raise FileNotFoundError
    csv_reader = reader(fp, delimiter=";", quotechar='"')
    for line, row in enumerate(csv_reader, start=1):
        if len(row) != 5:
            raise ParseError(
                file, f"Expected delimiter ';' in line number {line}: {row}"
            )
    fp.seek(0)
    try:
        df = pd.read_csv(fp, sep=";")
        fp.close()
    except FileNotFoundError:
        raise
    except pd.errors.ParserError as e:
        raise ParseError(file, e) from e
    except ValueError as e:
        raise ParseError(file, e) from e
    # Last column name expected of the form "Date#{username}"
    last_column = df.columns[-1]
    pos_username = last_column.find("Date#")
    if pos_username:
        raise ParseError(file, "Expecting last column name: 'Data#{username}'")
    else:
        username = last_column[5:].strip()
    if not username:
        raise ParseError(file, "Blank or only whitespace username")
    df = pd.DataFrame.rename(df, columns={last_column: "Date"})
    data = {"username": username, "scrobbles": df.to_dict(orient="records")}
    return data
