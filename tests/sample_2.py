from tabulate import tabulate
from memory_fm import parse_lastfmstats_json, loaders

with open("sample.json", "r") as fp:
    df = loaders.parse_json(fp)
scrobble_df = parse_lastfmstats_json.extract_scrobble_dataframe(df)
scrobble_df = parse_lastfmstats_json.verify_scrobbles_columns(scrobble_df, scrobbles_columns=['track', 'artist', 'album'])
table = tabulate(scrobble_df, tablefmt="grid", headers="keys")
print(table)
