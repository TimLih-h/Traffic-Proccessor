from contextlib import contextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import DEV_MODE, logger
from .schemes.packet import NetworkStats

last_info: NetworkStats = None
reset_dump = None


@contextmanager
async def lifespan(app: FastAPI):
    # startup'
    logger.info("Server started")
    yield
    # shutdown


app = FastAPI()
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
def load(body: NetworkStats):
    global last_info
    last_info = body
    
    if reset_dump is not None:
        last_info = last_info - reset_dump
    
    return {
        "status": "ok"
    }


@app.post('/reset')
def reset():
    global reset_dump
    reset_dump = last_info
    
    return {
        "status": "ok"
    }
