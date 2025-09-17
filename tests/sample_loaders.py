from pathlib import Path
from memoryfm.io._loaders import load_json, load_csv

# Works
#-----------------------------------------------
with open("sample.json", "r") as fp:
    data = load_json(fp)

print(data)

# Works 
#-------------------------------------------------

file_names_list = ["sample", "wrong_header", "no_username", "mismatch_delimiter"]

tests_dir = Path(__file__).resolve().parent

csv_dir = tests_dir / "data" / "csv"

for file_name in file_names_list:
    file = csv_dir / f"{file_name}.csv"
    print("---"*20)
    try:
        data = load_csv(file)
    except Exception as e:
        data = f"Error: {e}"
    print("File:", file)
    print(data)
    print()
# Works
#-------------------------------------------------

#data = load_csv("sample.csv")
#print(data["scrobbles"])
