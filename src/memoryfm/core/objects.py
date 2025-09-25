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
from memoryfm.errors import (
    InvalidDataError,
    SchemaError,
    InvalidTypeError,
    OperationNotAllowedError
)
from memoryfm.util.date_input_check import check_datetime
from memoryfm.core._validation import(
    validate_tz,
    validate_meta,
    validate_df,
    validate_text,
    meta_generator,
)

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

    def __str__(self) -> str:
        """Return String representation of Scrobble
        """
        if self.album == "NaN":
            self.album = None
        string_repr = (f"Timestamp: {self.timestamp}\n"
                       f"Track: {self.track}\n"
                       f"Artist: {self.artist}\n"
                       f"Album: {self.album}\n")
        return string_repr

    def validate_dict(data:dict) -> None:
        """
        Validate dict before creating Scrobble from dict
        """
        if not isinstance(data, dict):
            raise InvalidTypeError("Expecting dict type value.")
        keys = ["timestamp", "track", "artist"]
        for key in keys:
            if key not in data.keys():
                raise SchemaError(f"Missing key: {key}", key)
        check_datetime(data.get("timestamp"))

    
    def __dict__(self) -> dict:
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
    def from_dict(cls, data: dict) -> Self:
        """
        Construct Scrobble from dict
    
        Creates Scrobble object from dictionary.
    
        """
        cls.validate_dict(data)
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
 
    def to_dict(self) -> dict:
        """
         Get a canonical dict representation of Scrobble
        """
        return self.__dict__()

    def to_dataframe(self) -> pd.DataFrame:
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
    # Constructor
    def __init__(
        self,
        df: pd.DataFrame,
        *,
        meta: dict | None = None,
        update_meta: bool = True,
        username: str | None = None,
        tz: str | None = "Etc/UTC",
        source: str | None = "manual",
    ) -> Self:
        """ Create ScrobbleLog object from data.
        
        Parameters
        ----------
        df: pd.DataFrame
            DataFrame containing scrobble data.
            Columns:
                Required: ['timestamp', 'track', 'artist']
                Optional: ['album']
            Allowed values in columns:
            'timestamp': str, int, float, datetime, pd.Timestamp
            'track': str
            'artist': str
            A row with None type value in any column will be discarded.
            'album': 
                            
        If no 'album' column is found, a new column 'album' is added,
        with each value set to `None`.
        
        If meta is passed and valid, uses it do extract username, tz, source.
        An updated meta is generated from the data if `update_meta` is True.
        If not, tries to use `username`, `tz`, and `source` values (if passed)
        to generate `meta`
         
        """
        try:
            meta = validate_meta(meta)
        except (SchemaError, InvalidTypeError, InvalidDataError) as e:
            if meta is not None:
                print(f"Invalid meta passed: {e.error}."
                      "Generating meta from username, tz, and source.")
            self._df = validate_df(df, validate_tz(tz))
            self._meta = meta_generator(self._df, username, tz, source)
        else:
            if not update_meta:
                self._meta = meta
            else:
                self._df = validate_df(df, meta['tz'])
                self._meta = meta_generator(self._df,
                                            meta['username'],
                                            meta['tz'],
                                            meta['source'])

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, value) -> pd.DataFrame:
        self._df = validate_df(value, self._meta['tz'])

    @property
    def meta(self) -> dict:
        return self._meta

    @meta.setter
    def meta(self, value) -> dict:
        self._meta = validate_meta(value)
        if len(self._df) != self._meta['num_scrobbles']:
            raise InvalidDataError(
                "meta['num_scrobbles'] cannot be different from len(df)"
            )
        if self._meta['date_range']['start'] != self._df['timestamp'].min().isoformat():
            raise InvalidDataError(
                "start date must be in iso format and"
                "must not differ from the earliest scrobble date"
            )                           
        if self._meta['date_range']['end'] != self._df['timestamp'].max().isoformat():
            raise InvalidDataError(
                "start date must be in iso format and"
                "must not differ from the latest scrobble date"
            )

    @property
    def username(self) ->str | None:
        return self._meta['username']

    @username.setter
    def username(self, value) ->str | None:
        self._meta['username'] = validate_text(value, "username")

    @property
    def tz(self) ->str:
        return self._meta['tz']

    @tz.setter
    def tz(self, value) -> None:
        raise OperationNotAllowedError(
            "Timezone metadata cannot be changed without coverting"
            "df['timestamp'] values to required tz. "
            "To do so, use self.tz_convert."
        )
   
    def copy(self):
        return ScrobbleLog(df=self._df.copy(),
                           meta=dict(self._meta),
                           update_meta=False)

    # ------------------------------------------------------------------------
    # Rendering Methods

    def __len__(self) -> int:
        """Define len value for ScrobbleLog"""
        return len(self.df)

    def __str__(self) -> str:
        """
        Return String representation of ScrobbleLog
        """
        return self.to_markdown(tablefmt="pipe", maxcolwidths=20,
                                max_length=10, show_extra=False,
                                newest_first=False)

    def __bool__(self) -> bool:
        """Truth value"""
        return bool(len(self))

    # -----------------------------------------------------------------
    # Slicing and Indexing Methods

    @overload
    def __getitem__(self, index: int) -> Scrobble: ...
    @overload
    def __getitem__(self, index: slice) -> ScrobbleLog: ...

    def __getitem__(
        self,
        key: int | slice
    ) -> Scrobble | ScrobbleLog:
        """Access scrobbles by index or slice
        """
        if isinstance(key, slice):
            return ScrobbleLog(
                df=self.df[key],
                meta=self.meta,
                source=self.meta['source']
            )
        elif isinstance(key, int):
            d = self.df.iloc[key].to_dict()
            d["tz"] = self.tz
            return Scrobble.from_dict(d)
        else:
            raise InvalidTypeError("Expecting int or slice as key")

    # -----------------------------------------------------------------
    # Comparison methods

    def __eq__(self, other: ScrobbleLog) -> bool:
        """
        Define equality of two ScrobbleLogs
        """
        if not isinstance(other, ScrobbleLog):
            return False
        return self.to_dict() == other.to_dict()

    # -----------------------------------------------------------------
    # Iteration

    def __contains__(self, item: Scrobble) -> bool:
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
        scrobble: Scrobble,
        meta: dict | None,
        username: str,
        tz: str | None,
    ) -> Self:
        if isinstance(scrobble, Scrobble):
            return cls(df=scrobble.to_dataframe(), meta=meta,
                       username=username, tz=tz)

    def to_dict(self, orient: str = "records") -> dict:
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
    def from_dict(cls, data: dict, orient: str = "records") -> Self:
        """Create a ScrobbleLog from a canonical dict representation
        """
        if not isinstance(data, dict):
            raise InvalidTypeError("Expecting dict type value for 'data'")
        if "scrobbles" not in data.keys():
            raise SchemaError("Key 'scrobbles' not found", "scrobbles")
        df = pd.DataFrame(data["scrobbles"])
        return cls(
                df=df,
                meta=data.get("meta"),
                username=data.get("username"),
                tz=data.get("tz")
        )

    def to_markdown(
        self,
        file: PathLike | IO[str] | None = None,
        maxcolwidths: list[int] | None=None,
        tablefmt: str | None = "github",
        newest_first: bool = False,
        max_length: int | None = None,
        datetimefmt: str = "%Y-%m-%d %H:%M",
        showindex: bool = False,
        show_extra: bool = True
    ) -> str | None:
        """Write a nice looking ScrobbleLog in markdown using tabulate
        """
        df_new = self.df.copy().sort_values(by=['timestamp'],
                                            ascending = not newest_first)
        df_new["timestamp"] = (
                        df_new["timestamp"].dt.strftime(datetimefmt)
        )
        df_new = df_new.rename(str.capitalize, axis=1)
        if not len(self):
            df_table = "-----No scrobbles present-----"
        elif (
            max_length is None or
            len(self) <= max_length
        ):
            df_table = tabulate(df_new, headers="keys",
                             tablefmt=tablefmt,
                             maxcolwidths=maxcolwidths,
                             showindex=showindex)
        else:
            total = len(self)
            df1 = df_new.head()
            df2 = df_new.tail()
            dfsep = pd.DataFrame({"Timestamp":3*['...'],
                                  "Track":3*['...'],
                                  "Artist":3*['...'],
                                  "Album":3*['...']}
                                 )
            df = pd.concat([df1, dfsep, df2], ignore_index=True)
            df_table = tabulate(df, headers="keys", tablefmt=tablefmt,
                              maxcolwidths=maxcolwidths,
                              showindex=showindex)
            df_table = (df_table + "\n"
                     + f"Showing {max_length} out of {total} scrobbles") 
        if not show_extra:
            markdown = df_table
        else:
            markdown = (
                f"ScrobbleLog for username: {self.username}  \n"
                f"From {self.meta['date_range']['start']} to "
                f"{self.meta['date_range'].get('end')}\n\n"
                f"{df_table}"
            )
            
        from memoryfm.io._writers import _write_string
        return _write_string(markdown, file)

    @classmethod
    def from_json(
        cls, 
        file: PathLike | IO[str] | None = None,
    ) -> ScrobbleLog:
        """
        Create ScrobbleLog from canonical JSON.
        """
        from memoryfm.io._loaders import load_json
        canonical_dict = load_json(file)
        return ScrobbleLog.from_dict(canonical_dict)

    def to_json(
        self,
        file: PathLike | IO[str] | None = None,
        orient: str | None = "records",
        datetimefmt: str | None = "%Y-%m-%dT%H:%M:%S%z",
    ) -> str | None:
        """
        Write ScrobbleLog to canonical JSON format.
        """
        if not len(self):
            scrobbles = self.df.to_dict(orient="list")
        else:
            df_new = self.df.copy()
            df_new["timestamp"] = df_new["timestamp"].dt.strftime(datetimefmt)
            scrobbles = df_new.to_dict(orient=orient)
        data = {
            "meta": self.meta,
            "scrobbles": scrobbles
        }
        import json
        json_data = json.dumps(data)
        from memoryfm.io._writers import _write_string
        return _write_string(json_data, file)

    def to_csv( 
        self,
        file: PathLike | IO[str] | None = None,
        orient: str | None = "records"
    ) -> str | None:
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
    ) -> Self:
        if isinstance(scrobbles, Scrobble):
            df_2 = scrobbles.to_dataframe()
        elif (
            isinstance(scrobbles, list)
        ):
            scrobbles_data = [dict(scrobble) for scrobble in scrobbles]
            df_2 = pd.DataFrame(scrobbles_data)
        elif isinstance(scrobbles, ScrobbleLog):
            if (
                scrobbles.username == self.username and
                scrobbles.tz == self.tz
            ):
                df_2 = scrobbles.df.copy()
            elif scrobbles.tz != self.tz:
                df_2 = scrobbles.df.copy()
                df_2['timestamp'] = df_2['timestamp'].dt.tz_convert(self.tz)
            else:
                raise InvalidDataError("The usernames don't match")
        else:
            raise InvalidTypeError(
                "Expecting scrobbles value of type: "
                "Scrobble, list(Scrobble) list(dict) or ScrobbleLog"
            )
        self.df = pd.concat([self.df, df_2],
                            ignore_index=True)
        validate_df(self.df, self.tz)
        self.meta = meta_generator(self.df, self.username, self.tz)
        return self

    def tz_convert(self, tz: str | None, inplace=True) -> Self:
        if not inplace:
            df = self._df.copy()
            df['timestamp'] = df['timestamp'].dt.tz_convert(tz)
            meta = self._meta
            meta['tz'] = tz
            return ScrobbleLog(df, dict(self._meta))
        else:
            self._meta['tz'] = tz
            self._df = self._df['timestamps'].tz_convert(tz)
            return self

    # ------------------------------------------------------------------------
    # Filtering Methods

    def head(self, n: int | None = None) -> Self:
        """ Return ScrobbleLog for the first n scrobbles 
        """
        if n is None:
            n = 5
        return ScrobbleLog(self.df.head(n), meta=self.meta)

    def tail(self, n: int | None = None) -> Self:
        """ Return ScrobbleLog for the first n scrobbles 
        """
        if n is None:
            n = 5
        return ScrobbleLog(self.df.tail(n), meta=self.meta)

    def filter_by_date(
        self,
        start: str | pd.Timestamp | datetime.datetime | None = None,
        end: str | pd.Timestamp | datetime.datetime | None = None,
        unit : str | None = None,
        include_end: bool = True
    ) -> Self:
        """
        Filter ScrobbleLog by date.
        """
        if start is None:
            start = self.df["timestamp"].min()
        if end is None:
            end = self.df["timestamp"].max()
        start = check_datetime(start, tz=self.tz, unit=unit)
        end = check_datetime(end, tz=self.tz, unit=unit)
        # Consider the full day's data if no time (or 00:00) is passed
        if include_end and end.normalize() == end:  
            end = end + pd.Timedelta(days=1)
        if 'timestamp' not in self.df.columns:
            raise SchemaError("Expected column 'timestamp' missing",
                                     'timestamp')
        filter_start = self.df['timestamp'] >= start
        filter_end = self.df['timestamp'] < end
        filter_condition = filter_start & filter_end
        date_filtered_df = self.df[filter_condition]
        return ScrobbleLog(df=date_filtered_df, username=self.username,
                           tz=self.tz, source="filter")

    # -----------------------------------------------------------------
    # Charts Methods

    def top_charts(
        self: ScrobbleLog,
        kind: str = "track",
        n: int = 5
    ) -> pd.Series:
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
            raise TypeError("Expecting string type value for 'kind'")
        kind = kind.lower().strip().rstrip("s")
        if kind not in names_dict.keys():
            raise ValueError(
                f"'kind' must be a case-insensitive match for: {allowed_names}"
            )
        if not isinstance(n, int) or n < 0:
            raise ValueError("'n' must be a non-negative integer")
        df_new = self.df.copy()
        count_series = df_new[kind].value_counts()
        count_series.index.name = names_dict.get(kind)
        count_series.name = "Scrobbles"
        return count_series.head(n)
