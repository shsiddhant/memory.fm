# memory.fm

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fshsiddhant%2Fmemory.fm%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=for-the-badge&logo=python&logoColor=FFE873&color=4B8BBE)
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/shsiddhant/memory.fm/ci.yml?style=for-the-badge&logo=github&label=CI%20Pipeline)](https://github.com/shsiddhant/memory.fm/actions/workflows/ci.yml)


A small Python library and CLI tool for reading, analyzing, visualizing and exporting [Last.fm](https://www.last.fm) scrobble data.

Meant for anyone who obsesses over their music listening. Even if you aren't as obsessed, you are still welcome and encouraged to try it out.

**Inspired by my habit of repurposing music listening history as a medium to bring up memories.**

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
	- [CLI commands](#cli)
		- [Import Data](#import-data)
		- [List Imports](#list-imports)
		- [Load and Print](#load-and-print)
		- [Top Charts](#top-charts)
	- [Library Usage](#library-usage)
		- [Read and Parse](#read-and-parse)
		- [Filter by Dates](#filter-by-dates)
		- [Top Charts](#top-charts-1)
- [Roadmap](#roadmap)
- [Development](#development)
- [License](#license)
- [Acknowledgements](#acknowledgements)

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

## Installation

The package should soon be available on PyPI. For now, you can install 
directly from the repository with pip. 

```shell
$ pip install "memory.fm @ git+https://github.com/shsiddhant/memory.fm.git"
```

`ScrobbleLog` dates are timezone aware. If you want your timezone to be automatically
found from your system, you need to install the package with the optional dependency 
group `timezone`.

```shell
$ pip install "memory.fm[timezone] @ git+https://github.com/shsiddhant/memory.fm.git"
```

Requires **Python>=3.10**

## Quick Start

### CLI


Installing memory.fm gives you access to a command line tool ``memoryfm``. 
You can use it to manage your Last.fm scrobble data and Spotify listening data.

**Note:** Support for Apple Music exports is also planned. Check the [issue tracker](https://github.com/shsiddhant/memory.fm/issues) for updates.

##### Import Data
You can import your [Last.fm](https://www.last.fm.com>) data obtained from [lastfmstats](https://www.lastfmstats.com) like this:

```shell
$ memoryfm import lastfmstats /home/siddhant/Downloads/lastfmstats-lazulinoother.json --overwrite
Imported and saved to /home/siddhant/.local/share/memoryfm/imports/lazulinoother
```

Similarly, you can import Spotify listening history like this:

```shell
$ memoryfm import spotify ~/Downloads/my_spotify_data.zip --username sid-spotify
Imported and saved to /home/siddhant/.local/share/memoryfm/imports/sid-spotify
```

**Note:** You can have multiple imports, with the caveat that each username may only have one import.

##### List imports
To see all import usernames, use the ``list`` command.

```shell
$ memoryfm list
Scrobble Logs:
['sid-spotify', 'lazulinoother']
```

##### Load and Print
Printing scrobbles/listens and top charts is very simple. First you use the ``load`` command to load one of your imports.

```shell
$ memoryfm load lazulinoother
Loaded: lazulinoother
```

Now you can print your latest listens using the ``print`` command.

```shell
$ memoryfm print --max 5 --from '2024-05-05 3:30AM'
ScrobbleLog for username: lazulinoother  
From 2024-05-05 03:30 to 2025-10-23 09:40

| Timestamp        | Track             | Artist         | Album             |
|:-----------------|:------------------|:---------------|:------------------|
| 2024-05-05 03:30 | Will Anybody Ever | Sufjan Stevens | Javelin           |
|                  | Love Me?          |                |                   |
| 2024-05-05 03:34 | Will Anybody Ever | Sufjan Stevens | Javelin           |
|                  | Love Me?          |                |                   |
| 2024-05-05 03:38 | Will Anybody Ever | Sufjan Stevens | Javelin           |
|                  | Love Me?          |                |                   |
| 2024-05-05 03:42 | All I Need        | Radiohead      | In Rainbows       |
| 2024-05-05 03:45 | Asleep - 2011     | The Smiths     | Louder Than Bombs |
|                  | Remaster          |                |                   |
Showing first 5 out of 13483 scrobbles
```

##### Top Charts
The command `top` can be used to see your top tracks/artists/albums.

```shell
$ memoryfm top albums --max 5 --from 2024-05-05 --to 2024-05-10
| Album               |   Scrobbles |
|:--------------------|------------:|
| Either/Or           |         114 |
| The Glow, Pt. 2     |          85 |
| Songs About Leaving |          68 |
| Hospice             |          29 |
| Depression Cherry   |          22 |
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


## Roadmap

- [x] Support for loading Spotify listening history exports.
- [x] CLI commands for loading, printing, exporting, filters, top charts, etc. 
- [ ] Apple Music support.
- [ ] More analyses based on frequency, obsessive listens/streaks, duration (à la Spotify wrapped) etc.
- [ ] Visualizations and Plots.
- [ ] Spotify wrapped but make it nerdier.
- [ ] API support for Last.fm and Spotify.

Check the [issue tracker](https://github.com/shsiddhant/memory.fm/issues) for more details.

## Development

If you'd like to explore, improve, fix something, report bugs, or suggest any feature ideas  **memory.fm**, you are welcome to contribute.

To get started, you can have a look at the [issue tracker](https://github.com/shsiddhant/memory.fm/issues). If you want to report a bug or make a feature request, please open a [new issue](https://github.com/shsiddhant/memory.fm/issues/new/choose) using an appropriate template.

See [CONTRIBUTING](CONTRIBUTING.md) for a detailed overview of the contributing guidelines.


## License
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)


## Acknowledgements

Thanks to Felix Hagemans (https://github.com/felhag) for the fantastic [lastfmstats](https://www.lastfmstats.com).
