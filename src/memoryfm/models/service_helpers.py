from __future__ import annotations
from typing import Any
from dataclasses import dataclass
from pydantic import AliasPath, BaseModel, Field, ValidationError


@dataclass
class UserContext:
    user_id: int
    tz: str


class ScrobbleResponse(BaseModel):
    timestamp: int = Field(validation_alias=AliasPath("date", "uts"))
    track: str = Field(validation_alias=AliasPath("name"))
    artist: str = Field(validation_alias=AliasPath("artist", "#text"))
    album: str = Field(default="", validation_alias=AliasPath("album", "#text"))


def parse_lastfm_api_response(response_data: list[dict[str, Any]]):
    validated_data: list[tuple[int, str, str, str]] = []
    errors: list[str] = []
    error_count = 0
    for scrobble in response_data:
        if "@attr" in scrobble and scrobble["@attr"].get("nowplaying") == "true":
            continue
        try:
            scrobble_valid = ScrobbleResponse.model_validate(scrobble)
            validated_data.append(
                (
                    scrobble_valid.timestamp,
                    scrobble_valid.track,
                    scrobble_valid.artist,
                    scrobble_valid.album,
                )
            )
        except ValidationError as e:
            error_count += e.error_count()
            errors.extend([error.get("type") for error in e.errors()])
            continue

    return (validated_data, errors, error_count)
