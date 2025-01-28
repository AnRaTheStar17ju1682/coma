from typing import Annotated

from fastapi import HTTPException, Request, Depends, Query

from pydantic import ValidationError

import httpx

from config import settings

from utils import ImageUtils

from models_dto import OrderBy

from database.repositories import SQLAlchemyRepository
from database.database import engine, session_fabric

from interfaces import RepositoryInterface

from services.image_service import ImagesService
from services.search_service import SearchService

from redis_clients import redis_files, redis_text


async def redis_files_dependency():
    return redis_files


async def redis_text_dependency():
    return redis_text


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


async def tag_search_api_request(
    request: Request,
    order_by: Annotated[OrderBy, Query()] = OrderBy("post_date_desc"),
    include: Annotated[str, Query()] = "",
    exclude: Annotated[str, Query()] = "",
    page: Annotated[int, Query(ge=1)] = 1
) -> list[str]:
    search_params = {
        "order_by": order_by.value,
        "include_tags": include.split() if include else [],
        "exclude_tags": exclude.split() if exclude else [],
        "offset": 20*(page-1),
        "limit": 15
    }
    server_port = request.scope.get("server")[1]
    tag_search_url = str(request.url_for("tag_search").replace(port=server_port))
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(tag_search_url, json=search_params)
            item_hashes = response.json()
    except httpx.HTTPStatusError as err:
        raise HTTPException(status_code=err.response.status_code, detail=str(err))
    except httpx.RequestError as err:
        raise HTTPException(status_code=500, detail=str(err))
    
    return item_hashes