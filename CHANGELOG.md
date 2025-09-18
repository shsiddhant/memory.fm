## [Unreleased]

### Changed
- Renamed import package from memory_fm to memoryfm
- Replaced previous structure with class-based structure.
- Introduced `Scrobble` and `ScrobbleLog` classes as central objects classes.
    - Added standardized `dict` representations for both classes with `from_dict` and `to_dict` methods.
    - Added `__str__` methods for a readable string representation.
    - Added read/write methods for JSON/CSV formats.
    - Added `head` and `tail` method for printing first and last (n) scrobbles.
- Add Exception class `ScrobbleError(Exception)` and its subclasses `InvalidDataError`, `ParseError`, `SchemaError`.
- Added `from_lastfmstats` library function for creating ScrobbleLog from lastfmstats.com JSON/CSV exports.
- Separated file reader from loaders and put into util.
- Added type hints
- Added pytest as dev dependency

**Class: `ScrobbleLog`**
- Added dunder methods:
    - `__bool__`
    - `__contains__`
    - `__eq__`
    - `__getitem__`
    - `__iter__` returns an iterator: `ScrobbleLogIterator` instance
    - `__len__`
- Added `append` method to append `Scrobble`, list of `Scrobble`, or `ScrobbleLog`to existing `ScrobbleLog`
- Added `from_scrobble` method to create `ScrobbleLog` from username and `Scrobble`

**Pytest**
- Added and succesfully passed 22 pytest tests for `io` and core object classes.
