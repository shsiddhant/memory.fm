"""
Get top `n` tracks/artists/albums by number of scrobbles.
"""

import memoryfm as mfm
from pathlib import Path
file = Path(__file__).resolve().parent / "lastfmstats-lazulinoother.json"

start = input("Please enter the start date: ")
end = input("Please enter the end date: ")

#start = "2024-05-05"
#end = "2024-05-10"

scrobble_log = mfm.from_lastfmstats(file, "json", tz="Asia/Kolkata").filter_by_date(start, end)
#print(scrobble_log.head())

try:
    kind = input("Please enter the type of chart: ")
    n = int( input("Please enter the size of top chart: "))
except ValueError:
    raise
else:

    kind = kind.lower().strip().rstrip("s")
    kind_print_dict = {
        "track": "Tracks",
        "artist": "Artists",
        "album": "Albums"
    }
    count_series = scrobble_log.top_charts(kind, n)
    top_charts_markdown = count_series.to_markdown()
    kind_print = kind_print_dict.get(kind)
    print(f"""
Top 10 {kind_print} from {start} to {end}:

{top_charts_markdown}
""")
