from __future__ import annotations
import subprocess


def main():
    output = subprocess.check_output(
        ["streamlit", "run", "streamlitapp.py", "--server.address", "0.0.0.0"]
    )
    return output


if __name__ == "__main__":
    main()
