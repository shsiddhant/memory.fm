from typing import Any, Sequence
from pydantic import BaseModel, ConfigDict, TypeAdapter, ValidationError
from fastapi.exceptions import ResponseValidationError
from datetime import date, datetime
from math import log2

from memoryfm.models.service_enums import ChartKindColumn
from memoryfm.storage.streaks import StreakType


class ScrobblesCount(BaseModel):
    day: date
    value: int


class RecentActivity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    from_date: date
    to_date: date
    counts: list[ScrobblesCount]

    @classmethod
    def from_service_data(cls, data: tuple[date, date, Sequence[Any]] | None):
        schema = TypeAdapter(tuple[date, date, Sequence[Any]])
        if not data:
            raise ResponseValidationError(errors=[{"msg": "No data found for user."}])
        try:
            from_date, to_date, counts_seq = schema.validate_python(data)
        except ValidationError as e:
            raise ResponseValidationError(errors=e.errors())
        return cls(
            from_date=from_date,
            to_date=to_date,
            counts=[
                ScrobblesCount(day=row["Date"], value=row["Scrobbles"])
                for row in counts_seq
            ],
        )


class UserModel(BaseModel):
    user_id: int
    username: str


class SummaryDataModel(BaseModel):
    total_scrobbles: int
    days: int
    scrobbling_since: str
    scrobbles_per_day: int
    tracks: int
    artists: int
    albums: int


class SummaryModel(BaseModel):
    user: UserModel
    summary: SummaryDataModel


class TopChart(BaseModel):
    name: str
    scrobbles: int


class TimeSeriesData(BaseModel):
    day: date
    value: int | float


class AttachmentMoment(BaseModel):
    day: date
    value: float
    z_score: float
    name: str
    scrobbles: float
    total_scrobbles: float
    dominance: float


class YearRange(BaseModel):
    start: int
    end: int


class ListeningStreak(BaseModel):
    start: datetime
    end: datetime
    name: str
    subname: str | None
    length: int
    log_length: float
    kind: ChartKindColumn

    @classmethod
    def from_service_data(cls, kind: ChartKindColumn, data: StreakType | None):
        schema = TypeAdapter(StreakType)
        if not data:
            raise ResponseValidationError(errors=[{"msg": "No data found for user."}])
        try:
            if kind.subname_column is not None:
                start, end, name, length, subname = schema.validate_python(data)
            else:
                start, end, name, length = schema.validate_python(data)
                subname = None
        except ValidationError as e:
            raise ResponseValidationError(errors=e.errors())
        log_length = log2(length)
        return cls(
            start=start,
            end=end,
            name=name,
            subname=subname,
            length=length,
            log_length=log_length,
            kind=kind,
        )
