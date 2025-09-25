"""Module: memoryfm.utils.loaders
Handle JSON file inputs, possible errors, and parsing of JSON data into
a pandas DataFrame for further processing depending on the JSON source.
"""

from __future__ import annotations
import json
import pandas as pd
from typing import TYPE_CHECKING
from memoryfm.errors import ParseError
from memoryfm.util._file_handler import _file_opener


if TYPE_CHECKING:
    from typing import IO, Any
    from memoryfm._typing import PathLike


def load_json(file: PathLike | IO[str] = None) ->Any:
    r"""Read JSON file and return a pandas DataFrame, or raise an exception
      
    Parameters
    ----------
    file: PathLike object such as open( or file/file-like object
    
    """
    file_like = _file_opener(file, "r")
    try:
        data = json.load(file_like)
        file_like.close()
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as e:
        raise ParseError(file, f"{e.msg} at line {e.lineno} column {e.colno}")
    return data


def load_csv(file: PathLike | IO[str] = None) -> pd.DataFrame:
    """
    """ 
    file_like = _file_opener(file, "r")
    line_num = 0
    for line in file_like:
        col_list = line.split(";")
        if not line_num and len(col_list) != 5:
            raise ParseError(file, "Wrong delimiter or missing columns: "
                                   f"{len(col_list)}")
        elif not line_num:
            last_col = col_list[-1]
            pos_username = last_col.find("Date#")
            if pos_username:
                raise ParseError(file, "Expecting last column name: "
                                       "'Data#{username}'")
            else:
                username = last_col[5:].strip()
                if not username:
                    raise ParseError(file, "Blank or only whitespace username")
        if line_num and len(col_list) != 5:
            raise ParseError(file, "Expected delimiter ';' in line number "
                                   f"{line_num+1}: {line}")
        line_num = line_num + 1
    file_like.close()
    file_like = _file_opener(file)
    try:
        df = pd.read_csv(file_like, sep=";")
        file_like.close()
    except FileNotFoundError:
        raise
    except pd.errors.ParserError as e:
        raise ParseError(file, e) from e
    except ValueError as e:
        raise ParseError(file, e) from e
    # Last column name expected of the form "Date#{username}"
    last_column = df.columns[-1]
    df = pd.DataFrame.rename(df, columns={last_column: "Date"})
    data = {"username": username, "scrobbles": df.to_dict(orient="records")}
    return data
