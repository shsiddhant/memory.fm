from tabulate import tabulate
from memory_fm import parse_lastfmstats_json, check_json_validity

with open("sample.json", "r") as fp:
    df = check_json_validity.parse_json(fp)
scrobble_df = parse_lastfmstats_json.extract_scrobble_dataframe(df)
table = tabulate(scrobble_df, tablefmt="grid", headers="keys")
print(table)
