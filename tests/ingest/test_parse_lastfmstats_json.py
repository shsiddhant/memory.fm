from pathlib import Path
from tabulate import tabulate
from datetime import datetime as dt
from memory_fm import parse_lastfmstats_json, check_json_validity

project_dir = Path(__file__).resolve().parent.parent

file_name_list = [
    'empty_json', 'notfound', 'empty', 'invalid_json',
    'lastfmstats-lazulinoother_tail', 'wrong_column',
    'wrong_column_2', 'wrong_scrobbles_column_values', 'unordered'
    ]

files_separator = '-x-' * 40 + '|\n'
output_file = project_dir / 'ingest' / 'output_test_parse_lastfmstats_json.txt'
now = dt.now()
date_time_now = now.strftime("%Y-%m-%d %H:%M")
output = f"Output: {date_time_now}\n\n"

for name in file_name_list:
    orig_json_path = project_dir / 'data' / 'raw' / f'{name}.json'
    output = output + "\n" + files_separator + "\n"
    output = output + f"File: {orig_json_path}\n"
    
    try:
        df = check_json_validity.parse_json(orig_json_path)
        scrobble_df = parse_lastfmstats_json.extract_scrobble_dataframe(df)
    except OSError as e:
        output = output + e.strerror + "\n" 
    except check_json_validity.InvalidDataError as e:
        output = output + f"Invalid Data: {e}\n"
    else:
        table = tabulate(scrobble_df, tablefmt="grid", headers="keys")
        output = output + table + "\n"

print(table)
output_end = 'Output-End'.center(122, "-")
output = f"""
{output}

{output_end}

"""
print(output)

try:
    with open(output_file, 'a') as fp:
        fp.write(output)
        print("Output written to file:", output_file)

except OSError as e:
    print(e)
