from __future__ import annotations
import subprocess


def main():
    output = subprocess.check_output(["streamlit", "run", "streamlitapp.py"])
    return output


if __name__ == "__main__":
    main()
