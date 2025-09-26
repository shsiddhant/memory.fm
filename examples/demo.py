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
