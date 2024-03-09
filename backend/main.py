import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import create_engine, Session

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    pass
    # Execute
    yield
    # Shutdown
    pass


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
async def pong():
    return "pong"
