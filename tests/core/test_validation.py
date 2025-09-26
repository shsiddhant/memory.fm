import pytest

from memoryfm.core._validation import validate_tz, validate_meta
from memoryfm.errors import InvalidDataError, SchemaError, InvalidTypeError
from importlib.metadata import version

meta_valid = {
    "username": "sid",
    "tz": "Asia/Kolkata",
    "memory.fm_version": f"{version('memory.fm')}",
    "schema_version": 1,
    "num_scrobbles": 0,
    "date_range": {
        "start": None,
        "end": None
    },
    "source": "manual"
}

class TestValidateTZ:
    def test_tz_wrong_type(self):
        msg = r"Expecting string type value for .*"
        with pytest.raises(InvalidTypeError, match=msg):
            validate_tz(10)
    
    def test_tz_invalid_iana(self):
        msg = "Invalid IANA timezone string"
        with pytest.raises(InvalidDataError, match=msg):
            validate_tz("Asia")
    
    def test_tz_tzlocal(self):
        assert validate_tz()

    def test_tz_valid(self):
        assert validate_tz("Europe/London") == "Europe/London"


class TestValidateMeta:
    def test_no_dict(self):
        msg = "Expecting a dict type value"
        with pytest.raises(InvalidTypeError, match=msg):
            validate_meta([0])

    def test_missing_meta_key(self):
        msg = r"Missing key: .*"
        with pytest.raises(SchemaError, match=msg):
            validate_meta(
                {"username": "sid"}
            )

    def test_key_value_wrong_type(self):
        msg = r"Expecting .* type value for .*"
        with pytest.raises(InvalidTypeError, match=msg):
            validate_meta(
                {"username": 10,
                 "tz": "Etc/",
                 "num_scrobbles": 0

                 }
            )

    def test_whitespace_username(self):
        msg = "username cannot be just white-space"
        meta = meta_valid.copy()
        meta["username"] = " "
        with pytest.raises(InvalidDataError, match=msg):
            validate_meta(meta)

    def test_negative_num_scrobbles(self):
        msg = ("Expecting non-negative integer value for key: "
               "num_scrobbles")
        meta = meta_valid.copy()
        meta["num_scrobbles"] = -1
        with pytest.raises(InvalidDataError, match=msg):
            validate_meta(meta)

    def test_date_range_keys(self):
        msg = '.* key not found: start'
        meta = meta_valid.copy()
        meta["date_range"] = {}
        with pytest.raises(SchemaError, match=msg):
            validate_meta(meta)

    def test_date_range_wrong_value(self):
        msg = r".* must be None type"
        meta = meta_valid.copy()
        meta["date_range"] = {"start": None, "end": "2023"}
        with pytest.raises(InvalidDataError, match=msg):
            validate_meta(meta)

    def test_whitespace_source(self):
        msg = r"source cannot be just white-space"
        meta = meta_valid.copy()
        meta["source"] = ""
        with pytest.raises(InvalidDataError, match=msg):
            validate_meta(meta)
