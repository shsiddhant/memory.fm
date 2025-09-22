## [Unreleased]

## [v0.2.0] - 2025-09-22
### Added
- Add `top_charts` module to get top `n` tracks/artists/albums.
- Add `meta` and `source` attributes to `ScrobbleLog` to store metadata.
- Unit tests for the added `ScrobbleLog` attributes and methods.

### Changed
- Tighten `meta` validation.
- Ensure timezone localized and normalized timestamps.
- Preseve column schema when exporting empty `ScrobbleLog`
-
### Fixed
- Fix `ZoneInfo` missed exception `IsADirectoryError`.
- Fix hanging indents (PEP8)

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
