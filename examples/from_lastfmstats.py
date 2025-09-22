import memoryfm as mfm

scrobble_log = mfm.from_lastfmstats("sample.json", "json")
print(scrobble_log.head())

