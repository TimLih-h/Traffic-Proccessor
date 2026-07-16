from contextlib import asynccontextmanager
from pathlib import Path
import json

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime

from .core.config import DEV_MODE, logger
from .schemes.packet import NetworkStats
from .db import init_pool, close_pool, get_pool

last_info: NetworkStats = None
reset_dump = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server started")
    await init_pool()
    yield
    await close_pool()


app = FastAPI(lifespan=lifespan)
origins = ["*"]
static_dir = Path(__file__).parent / "static"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/root")
def root():
    return {"message": f"DEV_MODE is {DEV_MODE}"}


@app.get('/packets')
def packets():
    if last_info is not None:
        return last_info.model_dump()
    return {
        "status": "no information"
    }


@app.post('/load')
async def load(body: NetworkStats):
    global last_info
    last_info = body

    if reset_dump is not None:
        last_info = last_info - reset_dump

    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO traffic_history (ts, payload) VALUES (now(), $1::jsonb)",
            last_info.model_dump_json(),
        )

    return {"status": "ok"}


@app.get('/history')
async def history(
    limit: int = Query(100, le=1000),
    offset: int = 0,
    date_from: datetime | None = Query(None, description="ISO timestamp, inclusive"),
    date_to: datetime | None = Query(None, description="ISO timestamp, exclusive"),
):
    if date_from and date_to and date_from > date_to:
        raise HTTPException(400, "date_from must be earlier than date_to")

    pool = get_pool()
    query = "SELECT ts, payload FROM traffic_history WHERE 1=1"
    params = []

    if date_from:
        params.append(date_from)
        query += f" AND ts >= ${len(params)}"
    if date_to:
        params.append(date_to)
        query += f" AND ts < ${len(params)}"

    params.append(limit)
    query += f" ORDER BY ts DESC LIMIT ${len(params)}"
    params.append(offset)
    query += f" OFFSET ${len(params)}"

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    return [
        {"timestamp": row["ts"].isoformat(), "data": json.loads(row["payload"])}
        for row in rows
    ]


@app.post('/reset')
def reset():
    global reset_dump
    reset_dump = last_info
    
    return {
        "status": "ok"
    }
