import memoryfm
import json

scrobble_log = memoryfm.from_lastfmstats("lastfmstats-demo.csv", "csv",
                                         tz="Asia/Kolkata")
print(scrobble_log[6:9])
print()
print(scrobble_log.top_charts("albums", n=3).to_markdown())
print()

log_2 = memoryfm.ScrobbleLog.from_json("sample_2.json")
filtered = log_2.filter_by_date("2024-05-05 2:00AM", "2024-05-05 7:00AM")
print("Metadata for filtered ScrobbleLog:")
print(json.dumps(filtered.meta, indent=4))
