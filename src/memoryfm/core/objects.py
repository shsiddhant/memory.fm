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
from memoryfm.util.date_input_check import check_datetime
from memoryfm.core._meta import _validate_meta, _validate_tz, _meta_generator

if TYPE_CHECKING:
    from typing import IO, Self
    import datetime


# ---------------------------------------------------------------------
# Scrobble class - represents a single scrobble

@dataclass
class Scrobble:
    """
    Class representing a single scrobble
    """
    timestamp: pd.Timestamp
    track: str
    artist: str
    album: str | None = None

    def __str__(self) ->str:
        """Return String representation of Scrobble
        """
        if self.album == "NaN":
            self.album = None
        string_repr = (f"Timestamp: {self.timestamp}\n"
                       f"Track: {self.track}\n"
                       f"Artist: {self.artist}\n"
                       f"Album: {self.album}\n")
        return string_repr

    def _validate_dict(data:dict) ->None:
        """
        Validate dict before creating Scrobble from dict
        """
        if not isinstance(data, dict):
            raise TypeError("Expecting dict type value as data")
        keys = ["timestamp", "track", "artist"]
        for key in keys:
            if key not in data.keys():
                raise ScrobbleError(f"Missing {key}")
        check_datetime(data.get("timestamp"))

    
    def __dict__(self) ->dict:
        """
        Define a canonical dict representation of Scrobble
        """
        dict_repr = {
            "timestamp": self.timestamp,
            "track": self.track,
            "artist": self.artist,
            "album": self.album
        }
        return dict_repr
    
    # ------------------------------------------------------------------
    # IO Methods

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
 
    def to_dict(self) ->dict:
        """
         Get a canonical dict representation of Scrobble
        """
        return self.__dict__()

    def to_dataframe(self) ->pd.DataFrame:
        """Define a canonical pandas DataFrame representation of Scrobble
        """
        df_repr = pd.DataFrame(self.to_dict(), index=[0])
        return df_repr
    

# ---------------------------------------------------------------------
# Iterator

class ScrobbleLogIterator:
    def __init__(self, scrobble_log):
        """
        """
        self.scrobble_log = scrobble_log
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


# ---------------------------------------------------------------------
# ScroobleLog class - represents a scrobble log

class ScrobbleLog:
    """
    Class representing a scrobble log
    """
    
    # ----------------------------------------------------------------
    # Constructors
    def __init__(
        self,
        df: pd.DataFrame,
        username: str | None = None,
        tz: str | None = None,
        source: str | None = None,
        meta: dict | None = None
    ) ->None:
        """ Create ScrobbleLog object from data.
        """
        self.df = df
        if meta is not None:
            try:
                _validate_meta(meta)
            except (ValueError, SchemaError):
                print("Invalid meta. "
                      "Trying to generate a new meta from data")
            else:
                self.username = meta["username"]
                self.tz = meta["tz"]
                self.meta = meta
        else:
            if not isinstance(username, str):
                raise InvalidDataError("Expecting string type value for username")
            elif not username.strip():
                raise InvalidDataError("username only contains white-space")
            self.username = username
            if source is None:
                source = "manual"
            elif not isinstance(source, str):
                raise InvalidDataError("Expecting string type value for source")
            elif not source.strip():
                raise InvalidDataError("source only contains white-space")
            self.tz = tz
            _validate_tz(tz)
            self._validate_df()
            self.meta = _meta_generator(self.df, self.username,
                                        self.tz, source)

    #------------------------------------------------------------------
    # Validation

    def _validate_df(self) ->None:
        """
        Validate DataFrame
        """
        if not isinstance(self.df, pd.DataFrame):
            raise InvalidDataError("Expecting a pandas DataFrame as df")
        columns = ["timestamp", "track", "artist"]
        for column in columns:
            if column not in self.df.columns:
                raise SchemaError(
                    f"Required DataFrame column not found: {column}",
                    column
                )
        if not self.df.dropna.empty:
            from memoryfm.io._normalise import normalise_timestamps
            normalise_timestamps(self.df["timestamp"], tz=self.tz,
                                 unit="ms")
        if "album" not in self.df.columns:
            self.df["album"] = None
        self.df = self.df[["timestamp", "track", "artist", "album"]]
        self.df = self.df.replace('', None)
        
    # ------------------------------------------------------------------
    # Rendering Methods

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
            str_df = "-----No scrobbles present-----"
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
            f"ScrobbleLog for username: {self.username}\n"
            f"{str_df}\n"
            f"Time Zone: {self.tz}"
        )
        return string_repr 

    def __bool__(self) ->bool:
        """Truth value"""
        return bool(len(self))

    # -----------------------------------------------------------------
    # Slicing and Indexing Methods

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
            return ScrobbleLog(df=self.df[key], username=self.username,
                               tz=self.tz, source=self.meta["source"])
        elif isinstance(key, int):
            d = self.df.iloc[key].to_dict()
            d["tz"] = self.tz
            return Scrobble.from_dict(d)
        else:
            raise TypeError("Expecting int or slice as key")

    # -----------------------------------------------------------------
    # Comparison methods

    def __eq__(self, other: ScrobbleLog) ->bool:
        """
        Define equality of two ScrobbleLogs
        """
        if not isinstance(other, ScrobbleLog):
            return False
        return self.to_dict() == other.to_dict()

    # -----------------------------------------------------------------
    # Iteration

    def __contains__(self, item: Scrobble) ->bool:
        """
        Define in operator value for item in ScrobbleLog
        """
        if isinstance(item, Scrobble):
            return item.to_dict() in self.df.to_dict(orient="records")
        return False

    def __iter__(self):
        """
        """
        return ScrobbleLogIterator(self)

    # -----------------------------------------------------------------
    # IO Methods

    @classmethod
    def from_scrobble(
        cls,
        username: str,
        scrobble: Scrobble,
        tz: str | None
    ) ->Self:
        if isinstance(scrobble, Scrobble):
            return ScrobbleLog(df=scrobble.to_dataframe(),
                        username=username,
                        tz=tz)

    def to_dict(self, orient: str = "records") ->dict:
        """Canonical dict representation of ScrobbleLog
        """
        if not len(self):
            scrobbles = self.df.to_dict(orient="list")
        else:
            scrobbles = self.df.to_dict(orient=orient)
        data = {
            "meta": self.meta,
            "scrobbles": scrobbles
        }
        return data

    @classmethod
    def from_dict(cls, data: dict, orient: str = "records") ->Self:
        """Create a ScrobbleLog from a canonical dict representation
        """
        if not isinstance(data, dict):
            raise InvalidDataError("Expecting dict type value for 'data'")
        if "scrobbles" not in data.keys():
            raise SchemaError("Key 'scrobbles' not found", "scrobbles")
        df = pd.DataFrame(data["scrobbles"])
        return cls(
            df,
            data.get("username"),
            data.get("tz"),
            data.get("meta"),
            data.get("source")
        )

    def to_json(
        self,
        file: PathLike | IO[str] | None = None,
        orient: str | None = "records"
    ) ->str | None:
        """
        Write ScrobbleLog to JSON format.
        """
        import json
        if not len(self):
            scrobbles = self.df.to_dict(orient="list")
        else:
            df_new = self.df.copy()
            df_new["timestamp"] = df_new["timestamp"].apply(
                                                    pd.Timestamp.isoformat)
            scrobbles = df_new.to_json(orient=orient)
        data = {
            "meta": self.meta,
            "scrobbles": scrobbles
        }
        json_data = json.dumps(data)
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

    # -----------------------------------------------------------------
    # Transform Methods

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
        self.meta = _meta_generator(self.df, self.username, self.tz)
        return self

    # -----------------------------------------------------------------
    # Filtering Methods

    def head(self, n: int | None = None) ->Self:
        """ Return ScrobbleLog for the first n scrobbles 
        """
        if n is None:
            n = 5
        return ScrobbleLog(self.username, self.df.head(n), self.tz)

    def tail(self, n: int | None = None) ->Self:
        """ Return ScrobbleLog for the first n scrobbles 
        """
        if n is None:
            n = 5
        return ScrobbleLog(self.username, self.df.tail(n), self.tz)

    def filter_by_date(
        self,
        start: str | pd.Timestamp | datetime.datetime | None = None,
        end: str | pd.Timestamp | datetime.datetime | None = None,
        unit : str | None = None,
        include_end: bool = True
    ) ->Self:
        """
        Filter ScrobbleLog by date.
        """
        if start is None:
            start = self.df.iloc[0]["timestamp"]
        if end is None:
            end = self.df.iloc[len(self)-1]["timestamp"]
        start = check_datetime(start, tz=self.tz, unit=unit)
        end = pd.Timestamp(end, tz=self.tz, unit=unit)
        if include_end:
            end = end + pd.Timedelta(days=1)

        if 'timestamp' not in self.df.columns:
            raise SchemaError("Expected column 'timestamp' missing",
                                     'timestamp')
        filter_start = self.df['timestamp'] >= start
        filter_end = self.df['timestamp'] < end
        filter_condition = filter_start & filter_end
        date_filtered_df = self.df[filter_condition]
        return ScrobbleLog(df=date_filtered_df, username=self.username, tz=self.tz)

    # -----------------------------------------------------------------
    # Charts Methods

    def top_charts(
        self: ScrobbleLog,
        kind: str = "track",
        n: int = 5
    ) ->pd.Series:
        """
        Get top n tracks/artists/albums by number of scrobbles.
        """        
        names_dict = {
            "track": "Track",
            "artist": "Artist",
            "album": "Album"
        }
        allowed_names = [
        'track(s)',
        'artist(s)',
        'album(s)'
        ]
        if not isinstance(kind, str):
            raise TypeError("Expecting string type value for argument 'kind'")
        kind = kind.lower().strip().rstrip("s")
        if kind not in names_dict.keys():
            raise ValueError(
                f"'kind' must be a case-insensitive match for: {allowed_names}"
            )
        if not isinstance(n, int) or n < 0:
            raise ValueError
        df_new = self.df.copy()
        count_series = df_new[kind].value_counts()
        count_series.index.name = names_dict.get(kind)
        count_series.name = "Scrobbles"
        return count_series.head(n) 
