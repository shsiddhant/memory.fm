## [Unreleased]

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
