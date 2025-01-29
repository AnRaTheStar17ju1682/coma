import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models_orm import Base

from config import settings


logger = logging.getLogger(__name__)

try:
    database_url = settings.DATABASE_URL
    engine = create_async_engine(url=database_url, echo=settings.ENGINE_ECHO)
    logger.info("Database engine created successfully")
except Exception as err:
    logger.error("Failed to create engine: %s", err, exc_info=True)
    raise

session_fabric = async_sessionmaker(engine)


async def create_tables():
    logger.info("Starting database tables creation")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    
    except Exception as err:
        logger.error("Failed to create tables: %s", err, exc_info=True)
        raise


async def drop_tables():
    logger.warning("Starting database tables deletion")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.warning("Database tables dropped successfully")
    
    except Exception as err:
        logger.error("Failed to drop tables: %s", err, exc_info=True)
        raise