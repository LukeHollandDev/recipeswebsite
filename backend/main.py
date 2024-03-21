from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

from routers import recipes, users
from database import get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    pass
    # Execute
    yield
    # Shutdown
    pass


app = FastAPI(lifespan=lifespan)
app.include_router(recipes.router, dependencies=[Depends(get_session)])
app.include_router(users.router, dependencies=[Depends(get_session)])


@app.get("/ping")
async def pong():
    return "pong"
