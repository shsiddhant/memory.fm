# memory.fm (WIP)

Small toolkit for reading, analysing, visualizing and exporting last.fm scrobble data. Work in progress.
Implemented: Load JSON data obtained from lastfmstats.com and extract scrobble DataFrame.

**Inspired by personal music listening habits**

## Status: WIP
* JSON parsing and lastfmstats DataFrame extracter modules present.
* Exception handling in progress.
* Next goal: normaliser and markdown exporter modules.

## Installation
```shell
pip install -e .
```
## Usage (example)
```shell
git clone https://gitlab.com/sharmasiddhant/memory.fm/
cd memory.fm/tests
python sample.py
```
Output
```
+----+--------------------------------------+-----------------+---------------------+
|    | track                                | artist          | album               |
+====+======================================+=================+=====================+
|  0 | Good to Go                           | Elliott Smith   | Elliott Smith       |
+----+--------------------------------------+-----------------+---------------------+
|  1 | Moon sequel                          | Mount Eerie     | Dawn                |
+----+--------------------------------------+-----------------+---------------------+
|  2 | They'll Only Miss You When You Leave | Carissa's Wierd | Songs About Leaving |
+----+--------------------------------------+-----------------+---------------------+
```
Sample json file: sample.json
```json
{"username":"lazulinoother",
"scrobbles":[
	{"track":"Good to Go","artist":"Elliott Smith","album":"Elliott Smith"},
	{"track":"Moon sequel","artist":"Mount Eerie","album":"Dawn"},
	{"track":"They'll Only Miss You When You Leave","artist":"Carissa's Wierd","album":"Songs About Leaving"}
  ]
}
```
Sample script: sample.py

```python
from tabulate import tabulate                                                        
from memory_fm import parse_lastfmstats_json, check_json_validity                    
                                                                                     
with open("sample.json", "r") as fp:                                                 
    df = check_json_validity.parse_json(fp)                                          
scrobble_df = parse_lastfmstats_json.extract_scrobble_dataframe(df)                  
table = tabulate(scrobble_df, tablefmt="grid", headers="keys")                       
print(table)
```


