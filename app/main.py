from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "moods.db")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

os.makedirs(DATA_DIR, exist_ok=True)


@contextmanager
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mood_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                emotion TEXT NOT NULL,
                confidence REAL,
                client_time_utc TEXT,
                server_time_utc TEXT NOT NULL,
                user_agent TEXT,
                source TEXT
            )
            """
        )
        conn.commit()


class MoodEventIn(BaseModel):
    emotion: str = Field(description="Dominant emotion label, e.g., happy, sad")
    confidence: Optional[float] = Field(default=None, description="Confidence score in [0,1]")
    clientTime: Optional[str] = Field(default=None, description="Client ISO timestamp")
    sessionId: Optional[str] = Field(default=None, description="Browser session identifier")
    source: Optional[str] = Field(default="face-api.js", description="Detector source identifier")


class MoodAggregateOut(BaseModel):
    totals: Dict[str, int]
    windowMinutes: int
    sampleCount: int


app = FastAPI(title="Mood Tracker", version="1.0.0")

# Allow local development origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.post("/api/moods")
def post_mood(event: MoodEventIn, request: Request) -> JSONResponse:
    server_time_iso = datetime.now(tz=timezone.utc).isoformat()
    user_agent = request.headers.get("user-agent", "")

    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO mood_events (session_id, emotion, confidence, client_time_utc, server_time_utc, user_agent, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.sessionId,
                event.emotion,
                event.confidence,
                event.clientTime,
                server_time_iso,
                user_agent,
                event.source,
            ),
        )
        conn.commit()

    return JSONResponse({"status": "ok", "serverTime": server_time_iso})


@app.get("/api/moods/recent", response_model=MoodAggregateOut)
def get_recent(minutes: int = 60) -> MoodAggregateOut:
    minutes = max(1, min(24 * 60, minutes))
    cutoff = datetime.now(tz=timezone.utc) - timedelta(minutes=minutes)
    cutoff_iso = cutoff.isoformat()

    with get_db_connection() as conn:
        cur = conn.execute(
            """
            SELECT emotion, COUNT(*) as cnt
            FROM mood_events
            WHERE server_time_utc >= ?
            GROUP BY emotion
            ORDER BY cnt DESC
            """,
            (cutoff_iso,),
        )
        rows = cur.fetchall()
        cur2 = conn.execute(
            "SELECT COUNT(*) FROM mood_events WHERE server_time_utc >= ?",
            (cutoff_iso,),
        )
        sample_count = int(cur2.fetchone()[0])

    totals: Dict[str, int] = {str(emotion): int(cnt) for emotion, cnt in rows}
    return MoodAggregateOut(totals=totals, windowMinutes=minutes, sampleCount=sample_count)


@app.get("/")
def root() -> FileResponse:
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)


# Serve static assets under /static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
