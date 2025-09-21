# memory.fm (WIP)

[![Python](https://img.shields.io/badge/python-3.10%2B-4B8BBE?style=for-the-badge&logo=python&logoColor=%23FFE873)](https://www.python.org/)
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)

Small toolkit for reading, analysing, visualizing and exporting last.fm scrobble data. Work in progress.
Implemented: Load JSON/CSV data obtained from lastfmstats.com and get a ScrobbleLog object and use its methods.

**Inspired by personal music listening habits**

## Status: WIP
- [x] JSON/CSV parsing for lastfmstats.com exports.
- [x] Object classes `Scrobble` and `ScrobbleLog` for single scrobble and scrobble logs.
- [x] Canonical `dict` representations for object classes.
- [x] Print pretty looking `ScrobbleLog` using `tabular` package.
- [x] Filter `ScrobbleLog` by date.
- [x] Exception handling.
- [x] Pytest Tests
- [x] Top tracks/artist/album charts
- [ ] CLI implementation.
- [ ] Daily/Weekly track/album/artist obsession streaks.
- [ ] Documentation using asciidoc.

## Installation
Requires Python 3.10 or above
```shell
pip install -e .
```
## Usage (example)
```shell
git clone https://gitlab.com/sharmasiddhant/memory.fm/
cd memory.fm/examples
python from_lastfmstats.py
```
Output
```
Testing printing from JSON

Scrobble Logs for username: lazulinoother
+------------------+------------------------+-------------------+--------------------------+
| Timestamp        | Track                  | Artist            |          Album           |
+==================+========================+===================+==========================+
| 2025-09-10 01:30 | The Modern Leper       | Frightened Rabbit | The Midnight Organ Fight |
+------------------+------------------------+-------------------+--------------------------+
| 2025-09-10 01:34 | I Feel Better          | Frightened Rabbit | The Midnight Organ Fight |
+------------------+------------------------+-------------------+--------------------------+
| 2025-09-10 01:37 | Good Arms vs. Bad Arms | Frightened Rabbit | The Midnight Organ Fight |
+------------------+------------------------+-------------------+--------------------------+
| 2025-09-10 14:23 | Floating in the Forth  | Frightened Rabbit | The Midnight Organ Fight |
+------------------+------------------------+-------------------+--------------------------+

Testing printing from CSV

Scrobble Logs for username: lazulinoother
+------------------+----------------+--------------+---------------+
| Timestamp        | Track          |       Artist | Album         |
+==================+================+==============+===============+
| 2020-07-12 06:24 | Shades of Cool | Lana Del Rey | Ultraviolence |
+------------------+----------------+--------------+---------------+
| 2020-07-12 06:27 | Shades of Cool | Lana Del Rey | Ultraviolence |
+------------------+----------------+--------------+---------------+
| 2020-07-12 06:33 | Brooklyn Baby  | Lana Del Rey | Ultraviolence |
+------------------+----------------+--------------+---------------+
| 2020-07-12 06:37 | West Coast     | Lana Del Rey | Ultraviolence |
+------------------+----------------+--------------+---------------+
| 2020-07-12 06:43 | Sad Girl       | Lana Del Rey | Ultraviolence |
+------------------+----------------+--------------+---------------+
...  ...  ...  ...
...  ...  ...  ...
+------------------+----------------+----------------------+----------------------+
| 2020-07-12 07:05 | Flash          | Cigarettes After Sex | Cigarettes After Sex |
+------------------+----------------+----------------------+----------------------+
| 2020-07-12 07:09 | Truly          | Cigarettes After Sex | Cigarettes After Sex |
+------------------+----------------+----------------------+----------------------+
| 2020-07-12 07:15 | Black Beauty   | Lana Del Rey         |    Ultraviolence     |
+------------------+----------------+----------------------+----------------------+
| 2020-07-12 07:19 | Guns and Roses | Lana Del Rey         |    Ultraviolence     |
+------------------+----------------+----------------------+----------------------+
| 2020-07-12 07:23 | Florida Kilos  | Lana Del Rey         |    Ultraviolence     |
+------------------+----------------+----------------------+----------------------+
Showing 10 out of total 13 scrobbles
```
# LICENSE
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)

