"""Module memoryfm.core.objects
Defines object classes:
ScrobbleLog : represents a scrobble log
Scrobble    : (dataclass) represents a single scrobble.
"""

from __future__ import annotations
import pandas as pd
from dataclasses import dataclass
from typing import TYPE_CHECKING, overload
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

    def _validate_dict(data:dict) ->None:
        """Validate dict before creating Scrobble from dict
        """
        if not isinstance(data, dict):
            raise TypeError("Expecting dict type value as data")
        keys = ["timestamp", "track", "artist"]
        for key in keys:
            if key not in data.keys():
                raise ScrobbleError(f"Missing {key}")

    @classmethod
    def from_dict(cls, data: dict) ->Self:
        """
        Construct Scrobble from dict
    
        Creates Scrobble object from dictionary.
    
        """
        cls._validate_dict(data)
        if "album" not in data.keys():
            album = None
        else:
            album = data["album"]
        return cls(
            timestamp=pd.Timestamp(data["timestamp"]),
            track=data["track"],
            artist=data["artist"],
            album=album
        )

    
    def __dict__(self) ->dict:
        """Define a canonical dict representation of Scrobble"""
        dict_repr = {
            "timestamp": self.timestamp,
            "track": self.track,
            "artist": self.artist,
            "album": self.album,
        }
        return dict_repr

    def to_dict(self) ->dict:
        """Define a canonical dict representation of Scrobble"""
        return self.__dict__()

    def to_dataframe(self) ->pd.DataFrame:
        """Define a canonical pandas DataFrame representation of Scrobble
        """
        df_repr = pd.DataFrame(self.to_dict(), index=[0])
        return df_repr
    

class ScrobbleLogIterator:
    def __init__(self, scrobble_log):
        """
        """
        self.index = 0

    def __next__(self):
        """
        """
        if self.index < len(self.scrobble_log):
            scrobble = self.scrobble_log[self.index]
            self.index += 1
            return scrobble
        else:
            raise StopIteration


class ScrobbleLog:
    """Class representing a scrobble log."""
    def __init__(self, username: str, scrobbles_df: pd.DataFrame) ->None:
        self.username = username
        self.df = scrobbles_df
        self._validate_df()

    def _validate_df(self) ->pd.DataFrame:
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

    def __len__(self):
        """Define len value for ScrobbleLog"""
        return len(self.df)

    def __str__(self) ->str:
        """
        Return String representation of ScrobbleLog
        It is called by str() and print()
        """
        df_new = self.df.copy()
        df_new["timestamp"] = self.df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        df_new = df_new.rename(str.capitalize, axis=1)
        if not len(self):
            str_df = "----Empty---"
        elif len(self) <= 10:
            str_df = tabulate(df_new, headers="keys", tablefmt="grid",
                              showindex=False)
        else:
            total = len(self)
            str_df_head = tabulate(df_new.head(), headers="keys", tablefmt="grid",
                                   showindex=False)
            str_df_tail = tabulate(df_new.tail(), tablefmt="grid",
                                   showindex=False)
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

    def __bool__(self) ->bool:
        """Truth value"""
        return bool(len(self))

    @overload
    def __getitem__(self, index: int) ->Scrobble: ...
    @overload
    def __getitem__(self, index: slice) ->ScrobbleLog: ...

    def __getitem__(
        self,
        key: int | slice
    ) ->Scrobble | ScrobbleLog:
        """Access scrobbles by index or slice
        """
        if isinstance(key, slice):
            return ScrobbleLog(self.username, self.df[key])
        elif isinstance(key, int):
            return Scrobble.from_dict(self.df.loc[key].to_dict())
        else:
            raise TypeError("Expecting int or slice as key")

    def __eq__(self, other: ScrobbleLog) ->bool:
        """Define equality of two ScrobbleLogs"""
        if not isinstance(other, ScrobbleLog):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __contains__(self, item: Scrobble) ->bool:
        """Define `in` operator value for item in ScrobbleLog"""
        return item.to_dict() in self.df.to_dict(orient="records")

    def __iter__(self):
        """
        """
        return ScrobbleLogIterator(self)

    @classmethod
    def from_scrobble(cls, username: str, scrobble: Scrobble) ->Self:
        if isinstance(scrobble, Scrobble):
            dict_data = {"username": username,
                         "scrobbles": [scrobble.to_dict()]
                         }
            return cls.from_dict(dict_data)
            
    def append(
        self,
        scrobbles: Scrobble | list(Scrobble | dict) | ScrobbleLog
    ) ->Self:
        if isinstance(scrobbles, Scrobble):
            df_2 = scrobbles.to_dataframe()
        elif (
            isinstance(scrobbles, list)
        ):
            scrobbles_data = [dict(scrobble) for scrobble in scrobbles]
            df_2 = pd.DataFrame(scrobbles_data)
        elif isinstance(scrobbles, ScrobbleLog):
            if scrobbles.username == self.username:
                df_2 = scrobbles.df
            else:
                raise ScrobbleError("The usernames don't match")
        else:
            raise TypeError(
                "Expecting scrobbles value of type: "
                "Scrobble, list(Scrobble) list(dict) or ScrobbleLog"
            )
        self.df = pd.concat(
            [
                self.df,
                df_2
            ],
            ignore_index=True
        )
        self._validate_df()
        return self

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
                   pd.DataFrame(dict_data["scrobbles"]))

    def to_json(
        self,
        file: PathLike | IO[str] | None = None,
        orient: str | None = "records"
    ) ->str | None:
        """
        Write ScrobbleLog to JSON format.
        """
        df_json = self.df.to_json(orient=orient)
        json_data = f'{{"username":"{self.username}","scrobbles":{df_json}}}'
        from memoryfm.io._writers import _write_string
        return _write_string(json_data, file)

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
