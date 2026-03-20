from __future__ import annotations
import subprocess
import memoryfm
from importlib.resources import files
from memoryfm.cli import base_dir
from memoryfm._version import __version__


app_file = files(memoryfm) / "streamlit" / "streamlitapp.py"
dashboard_dir = base_dir / "dashboard"
dashboard_dir.mkdir(exist_ok=True)
local_streamlit_app = dashboard_dir / f"streamlitapp_{__version__}.py"
theme_config = """
    [theme]
    base="light"
    primaryColor="#b40b08"
    """


def main():
    streamlit_theme = dashboard_dir / ".streamlit"
    streamlit_theme.mkdir(exist_ok=True)
    config = streamlit_theme / "config.toml"
    if not config.is_file() or not config.read_text():
        config.write_text(theme_config)
    if not local_streamlit_app.is_file():
        app_code = app_file.read_text()
        for file in dashboard_dir.glob("streamlitapp_*.py"):
            file.rename(local_streamlit_app)
        local_streamlit_app.write_text(app_code)

    output = subprocess.check_output(
        [
            "streamlit",
            "run",
            f"{local_streamlit_app}",
            "--server.address",
            "0.0.0.0",
        ]
    )
    return output


if __name__ == "__main__":
    main()
