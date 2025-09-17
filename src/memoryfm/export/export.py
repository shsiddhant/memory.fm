"""Module: memoryfm.export
INCOMPLETE. DO NOT USE!
"""
import yaml
from .exceptions import SchemaError
from .ingest import parse_lastfmstats

def to_markdown(scrobble_data, md_file):
    try:
        keys = scrobble_data.keys()
    except AttributeError as e:
        raise SchemaError("Expected dict-like argument") from e
    if 'username' not in keys:
        raise SchemaError("Key not found", 'username')
    if 'scrobbles' not in keys:
        raise SchemaError("Key not found", 'scrobbles')
    
    parse_lastfmstats.verify_scrobbles_columns(scrobble_data, scrobbles_required_columns=['Date','Track', 'Artist', 'Album'])
    username = scrobble_data['username']
    scrobble_df = scrobble_data['scrobbles']
    df_1 = scrobble_df.loc[:, ['Date', 'Track', 'Album', 'Artist']]
    dict_data = {"username": username, "scrobbles":df_1.to_dict(orient='records'), "tags": "scrobbles"}
    scrobble_yaml = yaml.dump(dict_data)
    md_string = f"---\n{scrobble_yaml}\n---"
    md_file.write_text(md_string)
