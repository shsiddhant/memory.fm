import memoryfm as mfm

scrobble_log = mfm.from_lastfmstats("sample.json", "json")

print("\nTesting printing from JSON\n")
print(scrobble_log)

scrobble_log = mfm.from_lastfmstats("sample.csv", "csv")

print("\nTesting printing from CSV\n")
print(scrobble_log)
