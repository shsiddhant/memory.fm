# memory.fm

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fshsiddhant%2Fmemory.fm%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=for-the-badge&logo=python&logoColor=FFE873&color=4B8BBE)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/shsiddhant/memory.fm/ci.yml?style=for-the-badge&logo=github&label=CI%20Pipeline)](https://github.com/shsiddhant/memory.fm/actions/workflows/ci.yml)
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)

<blockquote style="text-align: center;">
 <b><i>music meets memory</i></b>
</blockquote>

**memory.fm** is a web application for exploring music listening history from Last.fm and Spotify.

Instead of focusing only on aggregate stats, it surfaces long-term and local patterns such as attachment, repetition, and obsessive listening, to help you revisit periods of your life through music.

>*✨Inspired by the idea of using music as a way to revisit memories.✨*


## Current Status

This is an active rewrite of memory.fm.

The current version includes:

- Last.fm import
- User overview dashboard
- Recent activity heatmap

More analytics and deeper insights are planned.


## Features

### Import and Manage Your Listening History

- Import your complete listening history from **Last.fm**
- Fast incremental sync after the first import.

### Stats and Analytics

**memory.fm** focuses on *how* you listened, not just *what* you listened to.

#### Overview

Get a clean summary of your music listening history.

<p align="center">
  <img src="screenshots/overview.png" height="600">
</p>


## Installation

```shell
pip install git+https://github.com/shsiddhant/memory.fm@rewrite
```

Requires **Python>=3.10**

## Running Locally

### Back-end

```shell
cd apps/
uvicorn api.main:app --reload
```

### Front-end

```shell
cd apps/web
npm install
npm run dev
```


## Roadmap

- [x] Last.fm Imports
- [x] User Overview
- [x] Recent Activity Heatmap
- [ ] Top Charts 
- [ ] Attachment Index
- [ ] Streaks and Streaks Timeline
- [ ] Time of Day / Season based analysis
- [ ] Memory Attachments and Timeline integration
- [ ] Spotify wrapped but make it nerdier

## Vision Preview (v0.8.5)  
  
An earlier experimental version of memory.fm explored deeper behavioral analytics and more experimental visualizations.  
You can check out a demo at: [https://memoryfm-demo.streamlit.app/](https://memoryfm-demo.streamlit.app/)

It introduced early versions of:

- Attachment Index (listening concentration over time)
- Streaks (intensity bursts in listening behavior)
- Streaks Timeline (color coded timeline of streaks across years)

The current rewrite is an architectural rebuild, focusing on:

- Stable import pipeline (Last.fm + future Spotify support) using SQLAlchemy.
- Modern FastAPI back-end and web UI (React)
- Extensible analytics layer

## Contributing

Contributions are welcome - whether you’d like to fix a bug, suggest an improvement, or propose new ideas for **memory.fm**.

If you find a bug or have a feature request, please open an issue using the appropriate template in the [issue tracker](https://github.com/shsiddhant/memory.fm/issues).

For detailed guidelines on contributing and development setup, see [CONTRIBUTING.md](CONTRIBUTING.md).


## License
This project is licensed under the [MIT License](LICENSE).


## Acknowledgements

Thanks to Felix Hagemans ([felhag](https://github.com/felhag)) for creating [lastfmstats](https://www.lastfmstats.com), which inspired parts of this
project.
