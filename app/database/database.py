from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from config import settings


database_url = settings.DATABASE_URL
engine = create_async_engine(url=database_url, echo=True)
session_fabric = async_sessionmaker(engine)