from __future__ import annotations
from typing import Literal, Annotated
from fastapi import FastAPI, Query
from memoryfm.db_services.stats import get_user_summary, get_top_charts

app = FastAPI()


@app.get("/user/{username}/summary")
def summary(username: str):
    return get_user_summary(username)


@app.get("/user/{username}/top={kind}")
def top_charts(
    username: str,
    kind: Literal["artist", "album", "track"],
    period: Annotated[
        int | Literal["all_time"],
        Query(
            description="Filter by period of ```period``` days. "
            "**Set to all_time to view all time top charts.**"
        ),
    ] = 7,
    limit: Annotated[
        int,
        Query(
            description="The number of items to return. **Set to -1 to fetch all**",
            ge=-1,
            examples=[0, 10, 50],
        ),
    ] = 10,
):
    return get_top_charts(username, kind, period, limit)
