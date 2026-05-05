from __future__ import annotations
from typing import Annotated, Any
from dataclasses import dataclass
from pydantic import (
    AliasPath,
    BaseModel,
    BeforeValidator,
    Field,
    ValidationError,
)
from memoryfm.errors import LastfmAPIError


@dataclass
class UserContext:
    user_id: int
    tz: str


class ScrobbleResponse(BaseModel):
    timestamp: int = Field(validation_alias=AliasPath("date", "uts"))
    track: str = Field(validation_alias=AliasPath("name"))
    artist: str = Field(validation_alias=AliasPath("artist", "#text"))
    album: str = Field(default="", validation_alias=AliasPath("album", "#text"))


def skip_now_playing(scrobbles: Any) -> list[ScrobbleResponse]:
    valid_scrobbles = []
    if isinstance(scrobbles, dict):
        valid_scrobbles.extend(convert_single_scrobble_to_list(scrobbles))
    elif isinstance(scrobbles, list):
        for scrobble in scrobbles:
            valid_scrobbles.extend(convert_single_scrobble_to_list(scrobble))
    return valid_scrobbles


def convert_single_scrobble_to_list(scrobble: Any) -> list[ScrobbleResponse]:
    if "@attr" in scrobble and scrobble["@attr"].get("nowplaying") == "true":
        return []
    try:
        scrobble_valid = ScrobbleResponse.model_validate(scrobble)
        return [scrobble_valid]
    except ValidationError:
        raise


FilteredScrobbles = Annotated[
    list[ScrobbleResponse],
    BeforeValidator(skip_now_playing),
]


class LastfmResponse(BaseModel):
    totalpages: int = Field(
        validation_alias=AliasPath("recenttracks", "@attr", "totalPages")
    )
    page: int = Field(validation_alias=AliasPath("recenttracks", "@attr", "page"))
    username: str = Field(validation_alias=AliasPath("recenttracks", "@attr", "user"))
    total_scrobbles: int = Field(
        validation_alias=AliasPath("recenttracks", "@attr", "total")
    )
    scrobbles: FilteredScrobbles = Field(
        validation_alias=AliasPath("recenttracks", "track")
    )


class LastfmErrorResponse(BaseModel):
    code: int = Field(validation_alias=AliasPath("error"))
    msg: str = Field(validation_alias=AliasPath("message"))


class LastfmUserInfoResponse(BaseModel):
    name: str = Field(validation_alias=AliasPath("user", "name"))
    url: str = Field(validation_alias=AliasPath("user", "url"))


def parse_lastfm_api_response(response_data: Any) -> LastfmResponse:
    try:
        return LastfmResponse.model_validate(response_data)
    except ValidationError:
        try:
            error_data = LastfmErrorResponse.model_validate(response_data).model_dump()
            raise LastfmAPIError(**error_data)
        except ValidationError:
            raise


def parse_lastfm_api_user_info(response_data: Any) -> LastfmUserInfoResponse:
    try:
        return LastfmUserInfoResponse.model_validate(response_data)
    except ValidationError:
        try:
            error_data = LastfmErrorResponse.model_validate(response_data).model_dump()
            raise LastfmAPIError(**error_data)
        except ValidationError:
            raise
