## [Unreleased]

### Added


### Changed


### Fixed


---

## [0.8.1] - 2026-01-01

### Changed

- Expose stats and viz modules to library's public API.

### Documentation

- Update and finish docstrings for the public API.
- Complete the docs with Quickstart Guide and API Reference.

---

## [0.8.0] - 2025-12-23

### Added
 
- Add an "Attachment Index" page with
    - a simple and clean summary.
    - a line chart of Attachment Index over time.
- Add a "Streaks" page with
    - longest streak details.
    - a timeline chart with color coded bands, each representing a streak.

### Changed

- Clean up the nested blocks on the "Top Charts" page.
- Remove unused code from the Streamlit app script.

### Fixed

- Fix disappearing sync scrobbles button and only display it when source is "last.fm".
- Fix mismatched bases for logarithm and exponent function in attachment index calculations.

---

## [v0.7.0] - 2025-12-06

### Added

- Add a basic Streamlit app with
	- a "Home" page to add, view, load, or delete imports.
	- an "Overview" page to view basic stats:
		- total/average scrobbles, tracks/artists/albums count
		- a bar graph showing scrobbles count by year
		- top 3 tracks/artists/albums
- Add a "Top Charts" tables with date filters and artist/album/track filters.
- Add support for importing using Last.fm username and API.
    - Add corresponding `import` subcommand `last.fm USERNAME` in CLI.
    - Add the same option to Streamlit app.
    - Show progress bar.
    - Add a sync button to update scrobbles for existing users. 

### Changed

- Add optional parameters `unit` and `source` to `normalise_lastfmstats`.
- Drop duplicates in `normalise_lastfmstats`.
- Add option to drop duplicates while appending scrobbles to a ScrobbleLog.

### Build

- Add a new dependency group 'all' to include all optional dependencies.

---

## [v0.5.0] - 2025-11-08

### Added

- Add CLI option to sort scrobbles by date.
- Add *Attachment Index* computer.
- Add *Streaks* computer.
- Add *Streaks Timeline* static and interactive plots.
- Add *Weighted Attachment Index* plots.

### Changed

- Move the functions `validate_tz` and `normalise_timestamps` to a  different module (`util.date_input_check`) to prevent circular imports.
- Replace exception raising in the CLI printer with printed error instead.

### Build

- Setup ruff and configure it in the `pyproject.toml`.
- Setup pre-commit hook for linting and formatting.
- Update the code to make sure it passes ruff checks.

---

## [v0.4.2] - 2025-10-14

### Added

- Add support for Spotify listening history zip instead of just the individual JSON files.

### Documentation

- Add docstrings for Input/Output methods and functions.

---


## [v0.4.1] - 2025-10-10

### Changed

- Replace unix style directory paths to `platformdirs` paths in CLI, to make it work across platforms.

---

## [v0.4.0] - 2025-10-10

### Added

- Add functions to  parse and normalise the Spotify listening history JSON
- Add a typer CLI app with the following commands.
    - `import lastfmstats`: import JSON/CSV from obtained from lastfmstats.com
    - `list`: list all imports
    - `load`: load an import
    - `loaded`: check loaded import
    - `print`: print `ScrobbleLog`
    - `top`: list top (n) artists/albums/tracks


### Changed

- Update validators to include the duration column in `ScrobbleLog` obtained from Spotify JSON data.
- Convert `None/NaN` and blanks to pandas `<NA>`.
- Reset index after validation.
- Update `meta` generator to include a  boolean`duration_present` key, to specify if the "duration" column is present or not.
- Update `meta` key `num_scrobbles` to `num_listens` if source is spotify.
- Update `schema_version: 2`.

### Fixed

- Fix missing f-string in `io/_normalise lineno 74`.
- Remove `duration` attribute from `Scrobble` class.
- Clean up `ScrobbleLog` method `to_markdown`  and handle the case when max length is 0.
- Fix undesired ParseError while loading a CSV if one of the values contains a semicolon.

### Build

- Update dependencies
    - Added: 
        - `typer` - CLI
        - `pyarrow` - Export to parquet
        - `wcwidth` - Correct widths for CJK characters.
- Optional dependencies groups:
    - doc : `sphinx`, `sphinx_design`, `pydata-sphinx-theme`, `numpydoc`, and `ipython`.
    - timezone : `tzlocal`
- Generate CLI executable/script from typer app using setuptools.
- Setup uv managed CI.

### Documentation

- Setup Sphinx generated docs with `autosummary` and `numpydoc`.
- Update docstrings for `ScrobbleLog` class.
- Add a quickstart guide.
    - Install instructions
    - Library Usage with examples using IPython.
    - CLI Usage with examples.
- Improve README and add a CONTRIBUTING guide.

---

## [v0.2.0] - 2025-09-22

### Added

- Add `top_charts` module to get top `n` tracks/artists/albums.
- Add `meta` attribute to `ScrobbleLog` to store metadata.
- Add methods:
    - `to_markdown` - Create nice-looking markdown exports.
    - `tz_convert` - Change timezone of a `ScrobbleLog`.
- Unit tests for the added `ScrobbleLog` attributes/methods, and validator.

### Changed

- Ensure timezone is localized and normalized timestamps.
- Preserve column schema when exporting empty `ScrobbleLog`.
- Use `to_markdown` method to redefine `ScrobbleLog` string representation so that it includes sorting, limiting column widths
- Change attributes to only include `_df` and `_meta`.
- Use `@property` decorator to define getter and setter methods `df`, `meta`, `username`, `tz`.
- Modify custom exceptions with better naming, in the `errors` module.
- Update modules & tests accordingly.

### Fixed

- Fix `ZoneInfo` missed exception `IsADirectoryError`.
- Fix hanging indents (PEP 8).

### Build/Internal

- Update build requirement:
    - Bump `setuptools>=80.0`.
    - Add dynamic versioning with `setuptools_scm`.
- Add `tzlocal` to dev, and extra (optional) dependencies.

---

## [v0.1.0] - 2025-09-18

### Added

- Introduce `Scrobble` and `ScrobbleLog` classes as central objects classes.
    - Add standardized `dict` representations for both classes with `from_dict` and `to_dict` methods.
    - Add dunder methods to `ScrobbleLog`:
        - `__str__`
        - `__bool__`
        - `__contains__`
        - `__eq__`
        - `__getitem__`
        - `__iter__`    (returns an iterator: `ScrobbleLogIterator` instance)
        - `__len__`
    - Add read/write methods for JSON/CSV formats.
    - Add methods: `head`, `tail`, `append`, `from_scrobble`, and `filter_by_date`
    - Add timezone attribute `tz`.
- Add Exception class `ScrobbleError(Exception)` and its subclasses `InvalidDataError`, `ParseError`, `SchemaError`.
- Add `from_lastfmstats` library function for creating ScrobbleLog from lastfmstats.com JSON/CSV exports.
- Add type hints.
- Unit tests for io and core methods.

### Changed

- Replace previous structure with class-based structure.
- Separate file reader from loaders and put into util.

---
