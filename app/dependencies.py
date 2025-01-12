from typing import Annotated

from fastapi import Depends


from config import settings

from utils import ImageUtils

from database.repositories import SQLAlchemyRepository

from database.database import engine, session_fabric

from interfaces import RepositoryInterface

from services.image_service import ImagesService
from services.search_service import SearchService


async def repository_dependency() -> RepositoryInterface:
    return SQLAlchemyRepository(engine, session_fabric)


async def image_service_dependency(
    repository: Annotated[RepositoryInterface, Depends(repository_dependency)]
) -> ImagesService:
    return ImagesService(repository, image_utils=ImageUtils(settings.IMAGE_SALT))


async def search_service_dependency(
    repository: Annotated[RepositoryInterface, Depends(repository_dependency)]
) -> SearchService:
    return SearchService(repository)