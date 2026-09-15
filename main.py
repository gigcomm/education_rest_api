import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import load_settings
from db.session import engine
from models.base import Base
from routers.category import category_router
from routers.tasks import task_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


config = load_settings()
app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)
app.include_router(router=category_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)