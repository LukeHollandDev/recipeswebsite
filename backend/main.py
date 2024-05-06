from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import recipes, users
from database import get_session

# Potentially don't include local host when running in PROD environment
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:5173",
    "https://localhost:5173",
    "http://lukeholland.dev",
    "https://lukeholland.dev",
    "http://recipes.lukeholland.dev",
    "https://recipes.lukeholland.dev",
]

app = FastAPI()
app.include_router(recipes.router, dependencies=[Depends(get_session)])
app.include_router(users.router, dependencies=[Depends(get_session)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def pong():
    return "pong"
