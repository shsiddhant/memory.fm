"""Module: memory_fm.utils.loaders
Handle JSON file inputs, possible exceptions, and parsing of JSON data into
a pandas DataFrame for further processing depending on the JSON source.
"""

import io
import json
import pandas as pd
from typing import IO
from pathlib import Path
from memory_fm import exceptions
PathLike = str | Path


def parse_json(json_file: PathLike | IO[str] = None) -> pd.DataFrame:
    r"""Read JSON file and return a pandas DataFrame, or raise an exception
      
    Parameters
    ----------
    json_file: PathLike object such as open( or file/file-like object
    
    """
    
    if json_file is None:
        raise TypeError("No Path or file specified")
    
    try:
        if isinstance(json_file, io.TextIOBase):
            json_data = json.load(json_file)
        else:
            with open(json_file, 'r') as fp:
                json_data = json.load(fp)
        base_df = pd.DataFrame(json_data)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as e:
        raise exceptions.ParseError(json_file, f"{e.msg} at line {e.lineno} column {e.colno}")
    except ValueError as e:
        raise exceptions.ParseError(json_file, f"{e}") from e

    return base_df
