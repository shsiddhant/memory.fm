#from tabulate import tabulate
#from memoryfm import parse_lastfmstats, loaders
#from memoryfm.io._normalise import normalise_lastfmstats
#
#with open("sample.json", "r") as fp:
#    df = loaders.parse_json(fp)
#scrobble_data = parse_lastfmstats.extract_scrobble_dataframe(df)
#parse_lastfmstats.verify_scrobbles_columns(scrobble_data, ['track', 'artist', 'album'])
#
#scrobble_data = normalise(scrobble_data)
#table = tabulate(scrobble_data, tablefmt="grid", headers="keys", showindex=False)
#print(table)
