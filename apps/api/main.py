from __future__ import annotations
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError
from apps.api.routers import analytics, user, websockets

from memoryfm.logging import configure_logging

if os.getenv("DEPLOYED_ENV") is None:
    load_dotenv()

configure_logging()

app = FastAPI()

origins = [
    "http://localhost:5173",
]

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173")

if FRONTEND_URL:
    origins.append(FRONTEND_URL)

origin_regex = r"https://memory-fm.*\.vercel\.app|http://localhost:5173"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics.router)
app.include_router(user.router)
app.include_router(websockets.router)


@app.exception_handler(ResponseValidationError)
async def pydantic_validation_exception_handler(
    request: Request, exec: ResponseValidationError
):
    return JSONResponse(status_code=422, content={"errors": exec.errors()})
