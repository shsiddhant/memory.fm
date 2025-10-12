"""Module memoryfm.core.objects
Defines object classes:
ScrobbleLog : represents a scrobble log
Scrobble: (dataclass) represents a single scrobble.
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
    from typing import (
        IO,
        Self,
        List
    )
    import datetime


# ---------------------------------------------------------------------
# Scrobble class - represents a single scrobble

@dataclass
class Scrobble:
    """
    Class representing a single scrobble/listen.

    Parameters
    ----------
    timestamp: pandas Timestamp
        Timestamp at which the track was scrobbled.
    track: str
        Name/title of the scrobbled track.
    artist: str
        Artist name for the scrobbled track.
    album: str, default None
        (Optional) Album name for the scrobbled track.

    See Also
    --------
    Scrobble.from_dict: Constructor from a dictionary with keys corresponding to each parameter (album is optional).
    """
    
    timestamp: pd.Timestamp
    track: str
    artist: str
    album: str | None = None

    def __str__(self) -> str:
        """
        Return a string representation of a Scrobble.
        """
        if self.album == "NaN":
            self.album = None
        string_repr = (
            f"Timestamp: {self.timestamp}\n"
            f"Track: {self.track}\n"
            f"Artist: {self.artist}\n"
            f"Album: {self.album}\n"
        )
        return string_repr

    def validate_dict(data:dict) -> None:
        """
        Check if the dictionary contains the required keys before creating 
        a Scrobble from it.
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
        Returns the canonical dict representation of a Scrobble.
        """
        dict_repr = {
            "timestamp": self.timestamp,
            "track": self.track,
            "artist": self.artist,
            "album": self.album,
        }
        return dict_repr
    
    # ------------------------------------------------------------------
    # IO Methods

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """
        Construct a Scrobble from a dictionary.
        """
        cls.validate_dict(data)
        return cls(
            timestamp=pd.Timestamp(data["timestamp"]),
            track=data["track"],
            artist=data["artist"],
            album=data.get("album"),
        )
 
    def to_dict(self) -> dict:
        """
         Returns the canonical dict representation of a Scrobble.
        """
        return self.__dict__()

    def to_dataframe(self) -> pd.DataFrame:
        """
        Returns a canonical pandas DataFrame representation of a Scrobble.
        """
        df_repr = pd.DataFrame(self.to_dict(), index=[0])
        df_repr = df_repr.replace({None:pd.NA})
        return df_repr
    

# ---------------------------------------------------------------------
# Iterator

class ScrobbleLogIterator:
    """
    Iterator class to iterate over a ScrobbleLog.
    """
    def __init__(self, scrobble_log):
        self.scrobble_log = scrobble_log
        self.index = 0

    def __next__(self):
        if self.index < len(self.scrobble_log):
            scrobble = self.scrobble_log[self.index]
            self.index += 1
            return scrobble
        else:
            raise StopIteration


# ---------------------------------------------------------------------
# ScrobbleLog class - represents a scrobble log

class ScrobbleLog:
    """
    Class representing a scrobble log, i.e. a sequence of scrobbles. 
    
    Parameters
    ----------
    df : pd.DataFrame

        |  A pandas DataFrame containing the scrobbles. It must have the 
           following columns:
        |  1. timestamp : ``str``, ``int``, ``datetime``, ``pd.Timestamp``
        |   This column contains timestamps of scrobbles. If ``int``, then 
            it will be assumed to be unix epoch (milliseconds).
        |  2. track : ``str``
        |   This column contains track names.
        |  3. artist : ``str``
        |   This column contains artist names.
        |  There are two optional columns:
        |  1. album : ``str``
        |   This column contains album names.
        |  2. duration : ``str``, ``int``, ``timedelta, ``pd.timedelta``
        |   This column contains durations of scrobbles/listens.

    meta : dict, default None

        |  A dictionary containing metadata with the following schema:
        |  "username" (``str``, ``None``) : Username for the ScrobbleLog.
        |  "tz" (``str``) : Timezone IANA string
        |  "num_scrobbles" (last.fm) or "num_listens" (``str``) : 
           Number of scrobbles/listens.
        |  "date_range" (``dict``) : A dictionary with keys,
        |    1. "start" (``str``, ``None``) : Date of first scrobble in isoformat
        |    2. "end" (``str``, ``None``) : Date of last scrobble in isoformat.
        |  "source" (``str``, ``None``) : Source of data (lastfmstats/spotify).
        |  "duration_present" (``bool``) : ``True`` if duration column present.
        |  "memoryfm.version" (``str``) : Version of `memory.fm`.
        |  "schema_version" (``int``) : Version of metadata schema.

    update_meta : bool, default True
        If ``True``, then meta is updated.
    username : str, default None
        username used while generating ``meta`` if no ``meta`` is passed.
    tz : str, default "Etc/UTC"
        tz value used while generating ``meta`` if no ``meta`` is passed.
    source : str, default "manual"
        source used while generating ``meta`` if no ``meta`` is passed.

    See Also
    --------
    meta_generator : Generates ``meta`` from ``username``, ``tz``, and ``source``
    
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
    ) -> None:
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
        """
        DataFrame containing scrobbles, normalised with required
        columns and dtypes.

        Returns
        -------
        pd.DataFrame
        """
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
                                max_length=10, show_extra=False,)

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
                df=self.df.iloc[key],
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
        newest_first: bool | None = None,
        max_length: int | None = None,
        datetimefmt: str = "%Y-%m-%d %H:%M",
        showindex: bool = False,
        show_extra: bool = True
    ) -> str | None:
        """
        Print ScrobbleLog in a nice looking markdown format.

        Parameters
        ----------
        file : PathLike or TextIOBase
            Path or file to write the markdown.

            * A pathlib path, or
            * A string corresponding to a path, such as
              ``/home/username/Documents/filename``, or
            * A TextIOBase object having a ``read()`` method.

            If ``None``, the markdown is returned as a string.
        maxcolwidths : list[int], default None
            A list of the maximum column widths allowed, in the same order as the
            ScrobbleLog DataFrame columns. To omit a column, put ``None`` at its
            position in the list.
        tablefmt : str, default 'github'
            The style of the table containing scrobbles. See `tabulate
            <https://pypi.org/project/tabulate/>`_ for options and details.
        newest_first : bool, default None

            * if ``True``, the ScrobbleLog is sorted by timestamps with newest
              scrobbles appearing at the top.
            * if ``False``, the ScrobbleLog is sorted by timestamps with oldest
              scrobbles appearing at the top.
            * if ``None``, the ScrobbleLog is not sorted.

        max_length : int, default None
            The maximum number of scrobbles to print.
        datetimefmt : str, default "%Y-%m-%d %H:%M"
            The datetime format to use for the 'Timestamp' values.
        showindex : bool, default ``False``
            Whether or not to show the index.
        show_extra : bool, default ``True``
            Whether or not show extra information like username, dates of the first
            and the last scrobbles.

        Returns
        -------
        None or str
            If file is ``None``, returns the markdown as a string. Returns ``None``
            otherwise.

        """
        df = self.df.copy()
        if newest_first is not None:
            df = df.sort_values(by=['timestamp'],
                                       ascending = not newest_first)
        from memoryfm.util.duration_convert import ms_to_time
        if 'duration' in df.columns:
            df["duration"] = ms_to_time(df["duration"])
        df = df.rename(str.capitalize, axis=1)
        if (max_length is not None and max_length <= 0) or not len(self):
            df_table = "-----No scrobbles present-----"
            return df_table
        elif (
            max_length is None or
            len(self) <= max_length
        ):
            bottom_text = ""
        else:
            total = len(self)
            listen = "scrobbles"
            if self.meta.get('source') == "spotify":
                listen = "listens"
            df = df.head(max_length)
            bottom_text = f"Showing newest {max_length} out of {total} {listen}" 
        df["Timestamp"] = (
                        df["Timestamp"].dt.strftime(datetimefmt)
        )
        if len(self):
            df_table = tabulate(df, headers="keys",
                                tablefmt=tablefmt,
                                maxcolwidths=maxcolwidths,
                                showindex=showindex)
        df_table = df_table + "\n" + bottom_text
        if not show_extra:
            markdown = df_table
        else:
            from datetime import datetime
            markdown = (
                f"ScrobbleLog for username: {self.username}  \n"
                f"From {datetime.strftime(self.df['timestamp'].min(), datetimefmt)} "
                f"to {datetime.strftime(self.df['timestamp'].max(), datetimefmt)}\n\n"
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
        Create ScrobbleLog from a canonical JSON.

        Parameters
        ---------- 
        file : PathLike or TextIOBase object.
            * A pathlib path, or
            * A string corresponding to a path, such as
              ``/home/username/Documents/filename``, or
            * A TextIOBase object having a ``read()`` method.

            The file must contain a valid :ref:`canonical JSON <canonical-json>`.

        Returns
        -------
        ScrobbleLog

        See Also
        --------
        :func:`to_json`
           Convert a ScrobbleLog to a canonical JSON.

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
        Convert a ScrobbleLog to a canonical JSON.

        A canonical JSON is of the form

        .. code-block:: python
           :caption: Canonical JSON format
           :name: canonical-json
           
           # A canonical JSON
           {
              "meta": ScrobbleLog.meta,
              "scrobbles": ScrobbleLog.df.to_dict(orient=orient)
           }

        Parameters
        ----------
        file : PathLike or TextIOBase object.
            * A pathlib path, or
            * A string corresponding to a path, such as
              ``/home/username/Documents/filename``, or
            * A TextIOBase object having a ``read()`` method.
        orient : str, default 'records'
            The style of values of ``scrobbles`` key. Allowed orient values are

            * ``records`` : list like ``[{column -> value}, ... , {column -> value}]``
            * ``index`` : dict like ``{index -> {column -> value}}``
            * ``columns`` : dict like ``{column -> {index -> value}}``

        datetimefmt : str, default '%Y-%m-%dT%H:%M:%S%z'
            A string representing a valid datetime format built from format codes.
            For example: '%Y-%m-%d' would be a date of the format YYYY-MM-DD.
            The default is the standard ISO 8601 with the UTC offset.

        Returns
        -------
        None or str
            If file is ``None``, returns the JSON string. Returns ``None`` otherwise.

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
        from memoryfm.io._writers import _write_string
        return _write_string(json.dumps(data), file)
    
 
    @classmethod
    def from_parquet(
        cls,
        meta_file: PathLike | IO[str],
        df_file: PathLike | IO [str],
        start: str | pd.Timestamp | datetime.datetime | None = None,
        end: str | pd.Timestamp | datetime.datetime | None = None,
        *,
        artists: List[str] | None = None,
        albums: List[str] | None = None,
        tracks: List[str] | None = None
    ) -> Self:
        """
        Create a ScrobbleLog from a :ref:`canonical parquet export
        <canonical_parquet>`.

        Parameters
        ----------
        meta_file : PathLike or TextIOBase object
            JSON file containing ScrobbleLog met as JSON string.
            The following types are accepted

            * A pathlib path, or
            * A string corresponding to a path, such as
              ``/home/username/Documents/filename``, or
            * A TextIOBase object having a ``read()`` method.
        df_file : PathLike or TextIOBase object 
            Parquet file containing the ScrobbleLog DataFrame.
            The following types are accepted

            * A pathlib path, or
            * A string corresponding to a path, such as
              ``/home/username/Documents/filename``, or
            * A TextIOBase object having a ``read()`` method.
        start : str, pd.Timestamp, datetime.datetime, default None
            The datetime to start reading the scrobbles.
        end : str, pd.Timestamp, datetime.datetime, default None
            The datetime to stop reading the scrobbles.

        artists : List[str], default None
            A list of strings containing artist names. It's a whitelist, i.e. only
            scrobbles with artist names from among the list are included.
        albums : List[str], default None
            A list of strings containing album names. It's a whitelist, i.e. only
            scrobbles with album names from among the list are included.
        tracks : List[str], default None
            A list of strings containing track names. It's a whitelist, i.e. only
            scrobbles with track names from among the list are included.

        Returns
        -------
        ScrobbleLog

        See Also
        --------
        :func:`to_parquet`
           Write ScrobbleLog to canonical parquet.

        """
        from pandas import read_parquet
        from memoryfm.io._loaders import load_json
        kind = {"artists": artists, "album": albums, "tracks": tracks}
        filter_df = [(k, 'in', v) for k, v in kind.items() if v is not None]
        if filter_df:
            df = read_parquet(df_file, filters=filter_df)
        else:
            df = read_parquet(df_file)
        meta = load_json(meta_file)
        return cls(df=df, meta=meta).filter_by_date(start, end)
            

    def to_parquet(
        self,
        meta_file: PathLike | IO[str],
        df_file:  PathLike | IO[str],
    ) -> None:
        """
        Write ScrobbleLog to canonical parquet.

        .. _canonical_parquet:
        
        The canonical parquet refers to a pair of files.

        * A JSON file : contains the ScrobbleLog meta
        * A parquet file : contains the ScrobbleLog DataFrame

        Parameters
        ---------- 
        meta_file : PathLike or TextIOBase object
            Path or file to save ScrobbleLog meta as a JSON string. The following
            types are accepted

            * A pathlib path, or
            * A string corresponding to a path, such as
              ``/home/username/Documents/filename``, or
            * A TextIOBase object having a ``read()`` method.
        df_file : PathLike or TextIOBase object 
            Path or file to save ScrobbleLog DataFrame as a parquet file.
            The following types are accepted

            * A pathlib path, or
            * A string corresponding to a path, such as
              ``/home/username/Documents/filename``, or
            * A TextIOBase object having a ``read()`` method.


        """
        import json
        from ..io._writers import _write_string
        _write_string(json.dumps(self.meta), meta_file)
        self.df.to_parquet(df_file)

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
        """ Return ScrobbleLog for the last n scrobbles 
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
                           tz=self.tz, source=self.meta.get("source"))

    # -----------------------------------------------------------------
    # Charts Methods

    def top_charts(
        self: ScrobbleLog,
        kind: str = "tracks",
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
