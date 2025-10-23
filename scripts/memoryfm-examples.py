from __future__ import annotations
import subprocess
from pathlib import Path

home = Path.home()
json_file = str(home / "Downloads" / "lastfmstats-lazulinoother.json")
examples = Path(__file__).resolve().parent.parent / "examples"

subcommands = {
    "import": ["import", "lastfmstats", json_file, "--overwrite"],
    "list": ["list"],
    "load": ["load", "lazulinoother"],
    "print": ["print", "--max", "5", "--from", "'2024-05-05 3:30AM'"],
    "top": [
        "top",
        "albums",
        "--max",
        "5",
        "--from",
        "2024-05-05",
        "--to",
        "2024-05-10",
    ],
}


def main():
    print(examples)
    if not examples.is_dir():
        raise FileNotFoundError("examples doesn't exist")
    for key, sub in subcommands.items():
        command = ["memoryfm"] + sub
        command_str = " ".join(command)
        print(command_str)
        output = subprocess.check_output(command).decode("utf-8")
        text = f"```shell\n$ {command_str}\n{output}```"
        output_file = Path(examples / f"{key}.md")
        with open(output_file, mode="w") as fp:
            fp.write(text)


if __name__ == "__main__":
    main()
