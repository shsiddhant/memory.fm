"""Module memoryfm.core.objects
Defines object classes:
ScrobbleLog : represents a scrobble log
Scrobble    : (dataclass) represents a single scrobble.
"""

from __future__ import annotations
import pandas as pd
from datetime import datetime as dt
from dataclasses import dataclass
from typing import TYPE_CHECKING
from tabulate import tabulate

from memoryfm._typing import PathLike
from memoryfm.errors import ScrobbleError, SchemaError, InvalidDataError

if TYPE_CHECKING:
    from typing import IO, Self

@dataclass
class Scrobble:
    """Class representing a single scrobble."""
    timestamp: pd.Timestamp
    track: str
    artist: str
    album: str | None = None

    def __str__(self) ->str:
        """Return String representation of Scrobble
        """
        if self.album == "NaN":
            album = ""
        string_repr = (f"Timestamp: {self.timestamp}\n"
                       f"Track: {self.track}\n"
                       f"Artist: {self.artist}\n"
                       f"Album: {album}\n")
        return string_repr

    @classmethod
    def from_dict(cls, data) ->Self:
        """
        Construct ScrobbleLog from dict
    
        Creates Scrobble object from dictionary.
    
        """
        keys = ["timestamp", "track", "artist"]
        for key in keys:
            if key not in data.get(key):
                raise ScrobbleError(f"Missing {key}")
        
        return cls(
            timestamp=pd.Timestamp(data["timestamp"]),
            track=data["track"],
            artist=data["artist"],
            album=data["album"]
        )

    def to_dict(self) ->dict:
        """Define a canonical dict representation of Scrobble"""
        dict_repr = {
            "timestamp": self.timestamp,
            "track": self.track,
            "artist": self.artist,
            "album": self.album
        }
        return dict_repr
    
class ScrobbleLog:
    """Class representing a scrobble log."""
    def __init__(self, username: str, scrobbles_df: pd.DataFrame) ->None:
        self.username = username
        self.df = scrobbles_df
        self._validate_df()

    def __len__(self):
        """Define len value for ScrobbleLog"""
        return len(self.df)

    def __str__(self) ->str:
        """
        Return String representation of ScrobbleLog
        It is called by str() and print()
        """
        df_new = self.df.copy()
        # Convert timestamp column to string
        df_new["timestamp"] = self.df["timestamp"].apply(
                                                    dt.strftime,
                                                    args=("%Y-%m-%d %H:%M",)
        )
        df_new = df_new.rename(str.capitalize, axis=1)
        if not len(self):
            str_df = "----Empty---"
        elif len(self) <= 10:
            str_df = tabulate(df_new, headers="keys", tablefmt="grid",
                              showindex=False, colalign=["left",
                                                         "left",
                                                         "left",
                                                         "center"
                                                         ])
        else:
            total = len(self)
            str_df_head = tabulate(df_new.head(), headers="keys", tablefmt="grid",
                                   showindex=False, colalign=["left",
                                                              "left",
                                                              "left"
                                                              "center"])
            str_df_tail = tabulate(df_new.tail(), tablefmt="grid",
                                   showindex=False, colalign=["left",
                                                              "left",
                                                              "left",
                                                              "center"])
            str_df = (
                f"{str_df_head}\n"
                "...  ...  ...  ...\n...  ...  ...  ...\n"
                f"{str_df_tail}\n"
                f"Showing 10 out of total {total} scrobbles"
            )
        string_repr = (
            f"Scrobble Logs for username: {self.username}\n"
            f"{str_df}"
        )
        return string_repr 
    
    def _validate_df(self) ->None:
        """
        """
        columns = ["timestamp", "track", "artist"]
        for column in columns:
            if column not in self.df.columns:
                raise SchemaError(
                    f"Required DataFrame column not found: {column}",
                    column
                )
        if "album" not in self.df.columns:
            self.df["album"] = None
            self.df = self.df[["timestamp", "track", "artist", "album"]]

    def head(self, n: int | None = None) ->Self:
        """ Return ScrobbleLog for the first n scrobbles 
        """
        if n is None:
            n = 5
        return ScrobbleLog(self.username, self.df.head(n))

    def tail(self, n: int | None = None) ->Self:
        """ Return ScrobbleLog for the first n scrobbles 
        """
        if n is None:
            n = 5
        return ScrobbleLog(self.username, self.df.tail(n))

    def to_dict(self, orient: str = "records") ->dict:
        """Canonical dict representation of ScrobbleLog
        """
        dict_data = {"username": self.username,
                     "scrobbles": self.df.to_dict(orient=orient)
                     }
        return dict_data

    @classmethod
    def from_dict(cls, dict_data: dict, orient: str = "records") ->Self:
        """Create a ScrobbleLog from a canonical dict representation
        """
        if not isinstance(dict_data, dict):
            raise InvalidDataError(
                "Expecting `dict` type object as 'dict_data'")
        for key in ["username", "scrobbles"]:
            if key not in dict_data.keys():
                raise InvalidDataError("Key '{key}' not found")
        return cls(dict_data["username"],
                   dict_data["scrobbles"])

    def to_json(
        self,
        file: PathLike | IO[str] | None = None,
        orient: str | None = "records"
    ) ->str | None:
        """
        Write ScrobbleLog to JSON format.
        """
        data = self.to_dict(orient=orient)
        from memoryfm.io._writers import _dict_to_json
        return _dict_to_json(data, file)

    def to_csv( 
        self,
        file: PathLike | IO[str] | None = None,
        orient: str | None = "records"
    ) ->str | None:
        """
        Write ScrobbleLog to CSV format.
        """
        data = self.to_dict(orient=orient)
        from memoryfm.io._writers import _dict_to_csv
        return _dict_to_csv(data, file)
