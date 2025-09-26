# memory.fm

[![Python](https://img.shields.io/badge/python-3.10%2B-4B8BBE?style=for-the-badge&logo=python&logoColor=%23FFE873)](https://www.python.org/)
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)

A small Python library and CLI application for reading, analyzing, visualizing and exporting [Last.fm](https://www.lastfm.com) scrobble data. Meant for anyone who obsesses over their music listening.

**Inspired by the habit of repurposing music listening history as a medium to bring up memories.**

## Features

- Parse Last.fm  JSON/CSV obtained from [lastfmstats](https://www.lastfmstats.com)
- API loosely modeled after [pandas](https://pypi.org/project/pandas/).
- Core object classes.
    - `Scrobble` - instance represents a single scrobble.
    - `ScrobbleLog` - instance represents a scrobble log. This class is the primary focus.
- Read and write canonical `dict` representations for object classes.
- `ScrobbleLog`:
    - Rich metadata such as username, timezone, and number of scrobbles, recorded in  `ScrobbleLog.meta` 
    - Use dunder methods for printing, slicing, iterating, and getting number of scrobbles.
    - Export to a canonical `JSON` which includes the metadata. Import the same to quickly re-create the `ScrobbleLog`.
    - Export to nice-looking markdown using [tabulate](https://pypi.org/project/tabulate/).
    - Filter `ScrobbleLog` by date.
    - Get top charts for tracks, artists, and albums.
    
- Should be Added Soon:
	- Support for Spotify listening history exports
	- CLI 

## Installation


```shell
pip install git+https://gitlab.com/sharmasiddhant/memory.fm.git
```

Requires **Python>=3.10**

## Quick Start

```python
import memoryfm
import json

# Parse lastfmstats.com CSV export and create a ScrobbleLog (optionally set timezone)
# (Note: Replace the file paths/names as per your need)
scrobble_log = memoryfm.from_lastfmstats("examples/lastfmstats-demo.csv", "csv",
                                         tz="Asia/Kolkata")
# Slicing
print(scrobble_log[6:9])
print("\nTop Charts")
# Top Charts and markdown export
print(scrobble_log.top_charts("albums", n=3).to_markdown())
# Parse Canonical JSON (exported using ScrobbleLog method: to_json)
log_2 = memoryfm.ScrobbleLog.from_json("examples/sample_export.json")
# Filter ScrobbleLog bu date/timestamp
filtered = log_2.filter_by_date("2024-05-05 2:00AM", "2024-05-05 7:00AM")
# Metadata
print("Metadata for filtered ScrobbleLog:")
print(json.dumps(filtered.meta, indent=4))
```

*Output*
```
| Timestamp        | Track            | Artist         | Album       |
|:-----------------|:-----------------|:---------------|:------------|
| 2025-09-12 04:37 | Porcelain Hands  | Weatherday     | Come In     |
| 2025-09-12 22:53 | So You Are Tired | Sufjan Stevens | Javelin     |
| 2025-09-12 22:58 | And So It Goes   | Billy Joel     | Storm Front |

Top Charts
| Album             |   Scrobbles |
|:------------------|------------:|
| Come In           |           7 |
| 69 Love Songs     |           4 |
| Once Twice Melody |           2 |
Metadata for filtered ScrobbleLog
{
    "username": "lazulinoother",
    "tz": "Asia/Kolkata",
    "num_scrobbles": 50,
    "date_range": {
        "start": "2024-05-05T02:21:36+05:30",
        "end": "2024-05-05T06:56:27+05:30"
    },
    "source": "filter",
    "memory.fm_version": "0.2.0",
    "schema_version": 1
}
```


# LICENSE
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)

