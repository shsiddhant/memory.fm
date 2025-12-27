# memory.fm

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fshsiddhant%2Fmemory.fm%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=for-the-badge&logo=python&logoColor=FFE873&color=4B8BBE)
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/shsiddhant/memory.fm/ci.yml?style=for-the-badge&logo=github&label=CI%20Pipeline)](https://github.com/shsiddhant/memory.fm/actions/workflows/ci.yml)


**memory.fm** is a Python library, CLI tool, and web-based dashboard for exploring music listening history from Last.fm and Spotify.

Instead of focusing only on aggregate stats, it surfaces long-term and local patterns such as attachment, repetition, and obsessive listening, to help you revisit periods of your life through music.

*Inspired by the idea of using music as a way to revisit memories.*

## Features

### Import and Manage Your Listening History

- Import your complete listening history from **Last.fm** and **Spotify**.
- Fast incremental sync after the first import.
- Supports JSON/CSV exports from [lastfmstats](https://www.lastfmstats.com).

### Stats and Analytics

**memory.fm** focuses on *how* you listened, not just *what* you listened to.

#### Top Charts

View your top artists, albums, and tracks. Filter them by weekly, monthly, and yearly periods, or a custom date range.

#### Attachment Index

The **Attachment Index** is a measure of how concentrated your listening was during a given period - whether you were deeply attached to a few tracks, albums, or artists, or broadly exploring.

#### Streaks

Detect periods of intense, repeated listening to a single artist, album, or track. These streaks often correspond to emotionally significant moments or phases.

With **Streaks Timeline**, you can view an interactive, color-coded timeline of your listening streaks. 


### Interface

You have two UI options:
- **Graphical Dashboard:** A user-friendly graphical dashboard that runs inside your web browser.
- **CLI:** A command line tool with more granular control for power users.

## Installation

The package should soon be available on PyPI. For now, you can install it directly from the repository using pip:

```shell
pip install "memory.fm @ git+https://github.com/shsiddhant/memory.fm.git"
```

Requires **Python>=3.10**

## Documentation

Full documentation for the Python library, and CLI will soon be
available at:

https://memory-fm.readthedocs.io


## Roadmap

- [x] Support for loading Spotify listening history exports
- [x] CLI commands for loading, printing, exporting, filters, top charts, etc.
- [x] API support for Last.fm
- [x] Attachment Index
- [x] Streaks and Streaks Timeline
- [ ] Time of Day / Season based analysis
- [ ] Memory Attachments and Timeline integration
- [ ] Spotify wrapped but make it nerdier
- [ ] Export options for data, visuals, and memory attachments
- [ ] Apple Music support

Check the [issue tracker](https://github.com/shsiddhant/memory.fm/issues) for more details.

## Contributing

Contributions are welcome - whether you’d like to fix a bug, suggest an improvement, or propose new ideas for **memory.fm**.

If you find a bug or have a feature request, please open an issue using the appropriate template in the [issue tracker](https://github.com/shsiddhant/memory.fm/issues).

For detailed guidelines on contributing and development setup, see [CONTRIBUTING.md](CONTRIBUTING.md).


## License
This project is licensed under the [MIT License](LICENSE).


## Acknowledgements

Thanks to Felix Hagemans ([felhag](https://github.com/felhag)) for creating [lastfmstats](https://www.lastfmstats.com), which inspired parts of this
project.
