import os

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.database import create_tables

from config import settings


content_path = settings.CONTENT_DIR


def create_folders_if_not_exists():
    thumbnails_path = content_path+"/thumbnails"
    
    if not os.path.exists(content_path):
        os.makedirs(content_path)
    if not os.path.exists(thumbnails_path):
        os.makedirs(thumbnails_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_folders_if_not_exists()
    await create_tables()
    yield
    pass