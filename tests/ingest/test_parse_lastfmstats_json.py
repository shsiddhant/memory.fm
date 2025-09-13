from pathlib import Path
from tabulate import tabulate
from datetime import datetime as dt
#import pandas as pd
from memory_fm import utils, ingest, exceptions, normalise
project_dir = Path(__file__).resolve().parent.parent

file_name_list = [
    'empty_json', 'notfound', 'empty', 'invalid_json',
    'lastfmstats-lazulinoother_tail', 'wrong_column',
    'wrong_column_2', 'wrong_scrobbles_column_values', 'unordered'
    ]
#file_name_list = ['notfound', 'empty_json', 'empty']
files_separator = '-x-' * 40 + '|\n'
output_file = project_dir / 'ingest' / 'output_test_parse_lastfmstats_json_new.txt'
now = dt.now()
date_time_now = now.strftime("%Y-%m-%d %H:%M")
output = f"Output: {date_time_now}\n\n"

for name in file_name_list:
    orig_json_path = project_dir / 'data' / 'raw' / f'{name}.json'
    output = output + "\n" + files_separator + "\n"
    output = output + f"File: {orig_json_path}\n"
    #print(output)
    #df = utils.loaders.parse_json(orig_json_path)
    try:
        df = utils.loaders.parse_json(orig_json_path)
        #print(type(df))
        scrobble_data = ingest.parse_lastfmstats.extract_scrobble_dataframe(df)
        ingest.parse_lastfmstats.verify_scrobbles_columns(scrobble_data)
    except FileNotFoundError as e:
        output = output + f"{e}" + "\n" 
    except exceptions.ParseError as e:
        output = output + f"{e}\n"
    except exceptions.SchemaError as e:
        output = output + f"{e}\n"
    except exceptions.ScrobbleError as e:
        output = output + f"{e}\n"
    else:
        scrobble_df = normalise.normalise_lastfmstats.normalise(scrobble_data['scrobbles'])
        
        table = tabulate(scrobble_df, tablefmt="grid", headers="keys")
        output = output + table + "\n"
#print(output)
print()
#print(table)
output_end = 'Output-End'.center(122, "-")
output = f"""
{output}

{output_end}
"""
print(output)

#try:
#    with open(output_file, 'a') as fp:
#        fp.write(output)
#        print("Output written to file:", output_file)
#
#except OSError as e:
#    print(e)
