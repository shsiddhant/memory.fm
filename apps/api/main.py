from __future__ import annotations
from fastapi import FastAPI

from .routers import analytics, user, websockets

app = FastAPI()

app.include_router(analytics.router)
app.include_router(user.router)
app.include_router(websockets.router)
