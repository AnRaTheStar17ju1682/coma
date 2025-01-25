from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models_orm import Base

from config import settings


database_url = settings.DATABASE_URL
engine = create_async_engine(url=database_url, echo=True)
session_fabric = async_sessionmaker(engine)


async def create_tables():
    engine.echo = False
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    engine.echo = True


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)