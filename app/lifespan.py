import os

import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.database import create_tables

from config import settings

from redis_clients import redis_files, redis_text


content_path = settings.CONTENT_DIR
logger = logging.getLogger(__name__)


def create_folders():
    thumbnails_path = content_path+"/thumbnails"
    
    logger.info("Starting folders creation")
    try:
        if not os.path.exists(content_path):
            os.makedirs(content_path)
        if not os.path.exists(thumbnails_path):
            os.makedirs(thumbnails_path)
    except Exception as err:
        logger.error("Try to check parent folder permissions - %s", err)
    logger.info("Folders succesfully created or already existed")


async def check_redis_health():
    try:
        await redis_text.ping()
        logger.info("Redis-text server is fine")
        await redis_files.ping()
        logger.info("Redis-files server is fine")
    except Exception as err:
        logger.error(err)
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Lifespan startup started")
    
    await check_redis_health()
    await create_tables()
    create_folders()
    
    logger.info("Lifespan startup successfully completed")
    
    yield