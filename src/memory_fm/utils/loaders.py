"""Module: memory_fm.ingest.check_json_validity
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
            log_json = json.load(json_file)
        else:
            with open(json_file, 'r') as fp:
                log_json = json.load(fp)
        
        log_df = pd.DataFrame(log_json)
    except OSError:
        raise
    except json.JSONDecodeError as e:
        raise exceptions.ScrobbleError(f"Not a valid JSON: {e.msg} at line {e.lineno} column {e.colno}")
    except ValueError as e:
        if "If using all scalar values, you must pass an index" in str(e):
            raise exceptions.ScrobbleError("Cannot create DataFrame. Expected non-scalar value for at least one of the keys")
    if not log_json:
        raise exceptions.EmptyJSONError(json_file)

    return log_df
