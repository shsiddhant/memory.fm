# memory.fm

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fshsiddhant%2Fmemory.fm%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=for-the-badge&logo=python&logoColor=FFE873&color=4B8BBE)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/shsiddhant/memory.fm/ci.yml?style=for-the-badge&logo=github&label=CI%20Pipeline)](https://github.com/shsiddhant/memory.fm/actions/workflows/ci.yml)
[![LICENSE: MIT](https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge)](LICENSE)

<div align="center">

***music meets memory***

</div>



**memory.fm** is a web application for exploring music listening history from Last.fm and Spotify.

Instead of focusing only on aggregate stats, it surfaces long-term and local patterns such as **attachment**, **repetition**, and **obsessive listening**, to help you revisit periods of your life through music.


## Preview

| Overview | Top Charts |
| -------- | -----------|
| <img src="screenshots/overview.png" width="600px" alt="User Overview Dashboard" />| <img src="screenshots/top_charts.png" width="600px" alt="User Overview Dashboard" />|

| Attachment Index | Attachment Moments Timeline |
| -------- | -----------|
| <img src="screenshots/attachment_index.png" width="600px" alt="Attachment Index" />| <img src="screenshots/attachment_timeline.png" width="600px" alt="Attachment Moments Timeline" />|

| Streaks Timeline - Artists | Streaks Timeline - Albums|
| -------------------------- | ------------------------ |
|<img src="screenshots/streaks_artists.png" width="600px" alt="Streaks Timeline - Artists" /> |<img src="screenshots/streaks.png" width="600px" alt="Streaks Timeline - Albums" />|

## Quick Start

### Clone and install

```
git clone https://github.com/shsiddhant/memory.fm.git
cd memory.fm
pip install .
```

### Run backend

```
cd apps
uvicorn api.main:app --reload
```

### Run frontend

```
cd apps/web
npm install
npm run dev
```

Then open:

http://localhost:5173


## Features

### Data Import & Sync

- Import full listening history from Last.fm
- Incremental sync after initial import
- (Planned) Spotify import support

### Behavioral Analytics

memory.fm focuses on **listening behavior modeling** instead of summary stats.

It surfaces patterns like:

- **Attachment**: how strongly you gravitate toward specific artists or tracks
- **Repetition**: how often you return to the same music
- **Obsessive listening:** short bursts of intense focus

These patterns help you rediscover periods of your life through music.

### Overview

A high-level snapshot of your listening history:

- Key summary statistics
- Activity heatmap (when you listened most)
- Quick preview of top artists, albums, and tracks

<img src="screenshots/overview.png" width="800px" alt="User Overview Dashboard" />

### Top Charts

Explore your favorites across time:

- Top artists, albums, and tracks
- Flexible time filters:
  - Weekly / Monthly / Yearly
  - Custom date ranges

<img src="screenshots/top_charts.png" width="800px" alt="User Top Charts" />

### Attachment

Measure how concentrated your listening is within a time period.

- High attachment -> focused listening (few artists on repeat)
- Low attachment -> more exploratory listening

<img src="screenshots/attachment_index.png" width="800px" alt="Attachment Index" />

#### Timeline of Attachment Moments

- Identify peaks in emotional or musical focus.
- Revisit phases where certain track, albums, or artists dominated your listening.

<img src="screenshots/attachment_timeline.png" width="800px" alt="Attachment Timeline" />

### Streaks

- Detect periods of intense, repeated listening to a single artist, album, or track. Streaks often correspond to emotionally significant moments or phases.

- With **Streaks Timeline**, you can view an interactive, color-coded timeline of your listening streaks. 

<img src="screenshots/streaks_timeline.webp" width="800px" alt="Streaks Timeline" />

### Coming Soon

- Time-of-day and seasonal patterns

## Roadmap

### 1. Data Imports

- [x] Last.fm imports
- [x] Incremental sync after initial import
- [ ] Spotify imports

### 2. Core Analytics Engine

- [x] Recent Activity and Summary
- [x] Top Charts (Artists / Albums / Tracks)
- [x] Rényi entropy
- [x] Attachment Index
- [x] Streaks
- [ ] Time of Day / Season based analysis

### 3. Front-end (React)

- [x] Overview dashboard
- [x] Activity heatmap
- [ ] Insights and visualization
	- [x] Attachment Index 
	- [x] Streaks Timeline
  - [ ] Streaks Cards

### 4. Ideas

- [ ] Memory Attachments and Timeline integration
- [ ] Spotify wrapped but make it nerdier


## Vision


An earlier experimental version (v0.8.5) of memory.fm explored deeper behavioral analytics and more experimental visualizations.

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

Contributions are welcome, especially in visualizations and front-end improvements.

If you find a bug or have a feature request, please open an issue using the appropriate template in the [issue tracker](https://github.com/shsiddhant/memory.fm/issues).

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup details.


## License
This project is licensed under the [MIT License](LICENSE).


## Acknowledgements

Thanks to Felix Hagemans ([felhag](https://github.com/felhag)) for creating [lastfmstats](https://www.lastfmstats.com), which inspired parts of this
project.
