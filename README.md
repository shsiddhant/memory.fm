# memory.fm (WIP)

Small toolkit for reading, analysing, visualizing and exporting last.fm scrobble data. Work in progress.
Implemented: Load JSON/CSV data obtained from lastfmstats.com and get a ScrobbleLog object.

**Inspired by personal music listening habits**

## Status: WIP
* JSON/CSV parsing and lastfmstats DataFrame extracter modules present.
* `ScrobbleLog` class and methods for string representation present.
* Canonical `dict` representation and `to_dict` and `from_dict` present.
* JSON/CSV read and write methods present.
* Exception handling added.
* Next goal: Add CLI implementation and pytest tests.

## Installation
```shell
pip install -e .
```
## Usage (example)
```shell
git clone https://gitlab.com/sharmasiddhant/memory.fm/
cd memory.fm/tests
python sample_lastfmstats.com.py
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
Sample json file: sample.json
```json
{"username":"lazulinoother",
"scrobbles":[{"track":"The Modern Leper",        "artist":"Frightened Rabbit","album":"The Midnight Organ Fight","albumId":"8bc361f4-0b80-35c9-8372-bb7c664d8d85","date":   1757467823000},{"track":"I Feel Better","artist":   "Frightened Rabbit","album":"The Midnight Organ Fight","albumId":"8bc361f4-0b80-35c9-8372-bb7c664d8d85","date":         1757468072000},{"track":"Good Arms vs. Bad Arms","artist":   "Frightened Rabbit","album":"The Midnight Organ Fight","albumId":"8bc361f4-0b80-35c9-8372-bb7c664d8d85","date":1757468274000},{"track":"Floating in the Forth","artist":"Frightened Rabbit","album":"The Midnight Organ Fight","albumId":"8bc361f4-0b80-35c9-8372-bb7c664d8d85","date":    1757514204000}]
}
```

Sample csv file: sample.csv
```csv
Artist│Album│AlbumId│Track│Date#lazulinoother
"Lana Del Rey"│"Ultraviolence"│"060d1168-7ea0-4290-9b05-ea3d23b14966"│"Shades of Cool"│"1594535082000"
"Lana Del Rey"│"Ultraviolence"│"060d1168-7ea0-4290-9b05-ea3d23b14966"│"Shades of Cool"│"1594535254000"
"Lana Del Rey"│"Ultraviolence"│"060d1168-7ea0-4290-9b05-ea3d23b14966"│"Brooklyn Baby"│"1594535609000"
"Lana Del Rey"│"Ultraviolence"│"060d1168-7ea0-4290-9b05-ea3d23b14966"│"West Coast"│"1594535866000"
"Lana Del Rey"│"Ultraviolence"│"060d1168-7ea0-4290-9b05-ea3d23b14966"│"Sad Girl"│"1594536184000"
"Cigarettes After Sex"│"I."│"50b51f4b-48ae-4f67-b94b-fe2f1aa87fb9"│"Dreaming of You"│"1594536486000"
"Cigarettes After Sex"│"I."│"50b51f4b-48ae-4f67-b94b-fe2f1aa87fb9"│"Starry Eyes"│"1594536692000"
"Cigarettes After Sex"│"Cigarettes After Sex"│"0c68495e-485d-4976-bb85-438249649d08"│"Sunsetz"│"1594537250000"
"Cigarettes After Sex"│"Cigarettes After Sex"│"0c68495e-485d-4976-bb85-438249649d08"│"Flash"│"1594537524000"
"Cigarettes After Sex"│"Cigarettes After Sex"│"0c68495e-485d-4976-bb85-438249649d08"│"Truly"│"1594537767000"
"Lana Del Rey"│"Ultraviolence"│"060d1168-7ea0-4290-9b05-ea3d23b14966"│"Black Beauty"│"1594538110000"
"Lana Del Rey"│"Ultraviolence"│"060d1168-7ea0-4290-9b05-ea3d23b14966"│"Guns and Roses"│"1594538380000"
"Lana Del Rey"│"Ultraviolence"│"060d1168-7ea0-4290-9b05-ea3d23b14966"│"Florida Kilos"│"1594538637000"
```
Sample script: sample_lastfmstats.py

```python
import memoryfm as mfm

scrobble_log = mfm.from_lastfmstats("sample.json", "json")

print("\nTesting printing from JSON\n")
print(scrobble_log)

scrobble_log = mfm.from_lastfmstats("sample.csv", "csv")

print("\nTesting printing from CSV\n")
print(scrobble_log)
```


