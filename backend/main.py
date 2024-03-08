import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel, Session

# required to import so SQLModel can create the tables
from models import Recipe, Ingredient, Instruction, Nutrient, Resource

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    # Execute
    yield
    # Shutdown
    pass


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
async def pong():
    return "pong"
