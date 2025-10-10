# memory.fm

[![Python](https://img.shields.io/badge/python-3.10%2B-4B8BBE?style=for-the-badge&logo=python&logoColor=%23FFE873)](https://www.python.org/)
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)

A small Python library and CLI tool for reading, analyzing, visualizing and exporting [Last.fm](https://www.last.fm) scrobble data.

Meant for anyone who obsesses over their music listening. Even if you aren't as obsessed, you are still welcome and encouraged to try it out.

**Inspired by my habit of repurposing music listening history as a medium to bring up memories.**

---

## Features

- Read and parse
    - [Last.fm](https://last.fm/)  JSON/CSV obtained from [lastfmstats](https://www.lastfmstats.com)
    - Spotify listening history exports.
- Use command line tool to
    - import Last.fm data.
    - import Spotify listening history.
    - see list of scrobbles/listens in any given period.
    - see top charts for tracks/artists/albums in any given period. 
- Library API loosely modeled after [pandas](https://pypi.org/project/pandas/).
- Core object classes.
    - `Scrobble` - instance represents a single scrobble.
    - `ScrobbleLog` - instance represents a scrobble log. This class is the primary focus.
- Read and write canonical `dict` representations for object classes.
- `ScrobbleLog`:
    - Rich metadata such as username, timezone, and number of scrobbles, recorded in  `ScrobbleLog.meta` 
    - Use dunder methods for printing, slicing, iterating, and getting number of scrobbles.
    - Export to a canonical JSON which includes the metadata. Import the same to quickly re-create the `ScrobbleLog`.
    - Export to nice-looking markdown using [tabulate](https://pypi.org/project/tabulate/).
    - Filter `ScrobbleLog` by date.
    - Get top charts for tracks, artists, and albums.
- Support for Spotify listening history exports

---

## Installation

The package should soon be available on PyPI. For now, you can install 
directly from the repository with pip. 

```shell
$ pip install "memory.fm @ git+https://gitlab.com/sharmasiddhant/memory.fm.git"
```

`ScrobbleLog` dates are timezone aware. If you want your timezone to be automatically
found from your system, you need to install the package with the optional dependency 
group `timezone`.

```shell
$ pip install "memory.fm[timezone] @ git+https://gitlab.com/sharmasiddhant/memory.fm.git"
```

Requires **Python>=3.10**

---

## Quick Start

### CLI


Installing memory.fm gives you access to a command line tool ``memoryfm``. 
You can use it to manage your Last.fm scrobble data and Spotify listening data.

**Note:** Support for Apple Music exports is also planned. Check issue tracker for updates.

You can import your [Last.fm](https://www.last.fm.com>) data obtained from [lastfmstats](https://www.lastfmstats.com) like this:

```shell
$ memoryfm import lastfmstats ~/Downloads/lastfmstats-siddhant.json
Imported and saved to /home/siddhant/.local/share/memoryfm/imports/siddhant
```

Similarly, you can import spotify listening history like this:

```shell
$ memoryfm import spotify ~/Downloads/Streaming_History_Audio_2025_2.json --username sid-spotify
Imported and saved to /home/siddhant/.local/share/memoryfm/imports/sid-spotify
```

**Note:** You can have multiple imports, with the caveat that each username may only have one import.

To see all import usernames, use the ``list`` command.

```shell
$ memoryfm list
Scrobble Logs:
['siddhant', 'sid-spotify']
```

Printing scrobbles/listens and top charts is very simple. First you use the ``load`` command to load one of your imports.

```shell
$ memoryfm load sid-spotify
Loaded: sid-spotify
```

Now you can print your latest listens using the ``print`` command.

```shell
$ memoryfm print --max-length 5
ScrobbleLog for username: sid-spotify
From 2025-06-03 21:33 to 2025-09-14 02:31

| Timestamp        | Track          | Artist          | Album             | Duration   |
|:-----------------|:---------------|:----------------|:------------------|:-----------|
| 2025-06-03 21:33 | These Days     | Nico            | Chelsea Girl      | 00:03:30   |
| 2025-06-03 21:40 | Re: Stacks     | Bon Iver        | For Emma, Forever | 00:06:41   |
|                  |                |                 | Ago               |            |
| 2025-06-03 21:44 | And So It Goes | Billy Joel      | Storm Front       | 00:03:37   |
| 2025-06-03 21:47 | Love Ridden    | Fiona Apple     | When The Pawn...  | 00:03:22   |
| 2025-06-03 21:54 | The Moon       | The Microphones | The Glow, Pt. 2   | 00:05:16   |
Showing newest 5 out of 3121 listens
```


### Library Usage

The library has two object classes:

1. Scrobble : Represents a single scrobbles/listen.
2. ScrobbleLog : Represents a sequence/log of scrobbles/listens.

#### Read and Parse

You can use `from_lastfmstats()` to read JSON/CSV downloads from
[lastfmstats](https://lastfmstats.com) to create a ``ScrobbleLog`` instance.
Optionally, you can set a timezone using IANA strings.

```shell 
In [1]: import memoryfm as mfm

In [2]: sclog = mfm.from_lastfmstats("../examples/lastfmstats-demo.csv",
   ...:                              file_type="csv",
   ...:                              tz="Asia/Kolkata")

In [3]: print(sclog[6:9])
| Timestamp        | Track            | Artist         | Album       |
|:-----------------|:-----------------|:---------------|:------------|
| 2025-09-12 04:37 | Porcelain Hands  | Weatherday     | Come In     |
| 2025-09-12 22:53 | So You Are Tired | Sufjan Stevens | Javelin     |
| 2025-09-12 22:58 | And So It Goes   | Billy Joel     | Storm Front |
```

#### Filter by Dates

You can filter a ``ScrobbleLog`` by dates using the method `ScrobbleLog.filter_by_date()`. You may pass the time alongside the date. 
The end date is included by default.
If you'd like to exclude the end date, pass ``include_end = False`` to the method.

```shell
In [4]: print(sclog.filter_by_date(start="2025-09-12 10 PM",
   ...:                            end="2025-09-13",
   ...:                            include_end = False))
| Timestamp        | Track            | Artist         | Album            |
|:-----------------|:-----------------|:---------------|:-----------------|
| 2025-09-12 22:53 | So You Are Tired | Sufjan Stevens | Javelin          |
| 2025-09-12 22:58 | And So It Goes   | Billy Joel     | Storm Front      |
| 2025-09-12 23:16 | I Know           | Fiona Apple    | When the Pawn... |
```

#### Top Charts

Using the method `ScrobbleLog.top_charts()`,  you can obtain top `n` 
tracks/artists/albums from a ``ScrobbleLog``. The method returns a pandas Series,
with name: ``Scrobbles``. 


```shell
In [5]: print(sclog.top_charts(kind="album",
   ...:                        n=3).to_markdown())
| Album             |   Scrobbles |
|:------------------|------------:|
| Come In           |           7 |
| 69 Love Songs     |           4 |
| Once Twice Melody |           2 |
```
---

## Roadmap

- [x] Support for loading Spotify listening history exports.
- [x] CLI commands for loading, printing, exporting, filters, top charts, etc. 
- [ ] Apple Music support.
- [ ] More analyses based on frequency, obsessive listens/streaks, duration (à la Spotify wrapped) etc.
- [ ] Visualizations and Plots.
- [ ] API support for Last.fm and Spotify.

---


## Development

If you'd like to explore, improve, fix something, report bugs, or suggest any feature ideas  **memory.fm**, you are welcome to contribute.

To get started, you can have a look at the [issues tracker](https://gitlab.com/sharmasiddhant/memory.fm/-/issues). If you want to report a bug or make a feature request or suggestions, please open a [new issue](https://gitlab.com/sharmasiddhant/memory.fm/-/issues/new?type=ISSUE) using an appropriate template.

See [[CONTRIBUTING]] for a detailed overview of the contributing guidelines.

---

## License
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)

---

## Acknowledgments

Thanks to Felix Hagemans (https://github.com/felhag) for the fantastic [lastfmstats](https://www.lastfmstats.com).

---
