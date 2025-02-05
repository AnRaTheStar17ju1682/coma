from typing import Annotated

import json

from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, Form, Body

from sqlalchemy.exc import IntegrityError, NoResultFound

from psycopg.errors import UniqueViolation

from redis.asyncio import Redis

from models_dto import (
    ItemPostDTO,
    ItemPutDTO,
    ItemSearchParamsDTO,
    FileSavingParamsDTO
)

from services.image_service import ImagesService
from services.search_service import SearchService

from routes.dependencies import image_service_dependency, search_service_dependency, redis_text_dependency


router = APIRouter(prefix="/api/items", tags=["api"])


@router.post("/", status_code=201)
async def upload_item(
    item: Annotated[ItemPostDTO, Form()],
    image_service: Annotated[ImagesService, Depends(image_service_dependency)],
    background_tasks: BackgroundTasks,
    save_mode: Annotated[FileSavingParamsDTO, Depends()]
):
    try:
        item_hash, item_id = await image_service.post_image(item, save_mode)
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            raise HTTPException(
                status_code=409,
                detail={
                    "msg": "An item with this hash already exists, change old post, instead of creating new",
                    "item_hash": err.params["item_hash"]
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Database error"
            )
    return {"created_item_hash": item_hash, "created_item_id": item_id}


@router.delete("/{item_hash}", status_code=200)
async def delete_item(
    item_hash: str,
    image_service: Annotated[ImagesService, Depends(image_service_dependency)]
):
    try:
        deleted_item_id = await image_service.delete_from_disk(image_hash=item_hash)
        
        return {"deleted_item_hash": item_hash, "deleted_item_id": deleted_item_id}
    except NoResultFound as err:
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "An Item with this hash does not exists",
                "hash": item_hash
            }
        )


@router.get("/{item_hash}", status_code=200)
async def get_item_data(
    item_hash: str,
    image_service: Annotated[ImagesService, Depends(image_service_dependency)],
    r: Annotated[Redis, Depends(redis_text_dependency)]
):
    r_key =  "item_data:" + item_hash
    
    try:
        if item_data_json := await r.get(r_key):
            pass
        else:
            item_data = await image_service.get_image_data(image_hash=item_hash)
            item_data_json = item_data.model_dump_json()
            
            await r.set(r_key, item_data_json, ex=5)
        
        return item_data_json
    except NoResultFound as err:
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "An Item with this hash does not exists",
                "hash": item_hash
            }
        )


@router.put("/{item_hash}", status_code=200)
async def upadte_item_data(
    item_hash: str,
    item: Annotated[ItemPutDTO, Body()],
    image_service: Annotated[ImagesService, Depends(image_service_dependency)]
):
    try:
        updated_item_new_id = await image_service.update_image_data(item_hash, item)
        
        return {"updated_item_hash": item_hash, "updated_item_new_id": updated_item_new_id}
    except NoResultFound as err:
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "An Item with this hash does not exists",
                "hash": item_hash
            }
        )


@router.post("/tag_search")
async def tag_search(
    search_params: ItemSearchParamsDTO,
    search_service: Annotated[SearchService, Depends(search_service_dependency)],
    r: Annotated[Redis, Depends(redis_text_dependency)]
) -> list[str]:
    r_key = "search:" + search_params.model_dump_json()
    
    if item_hashes := await r.get(r_key):
        item_hashes = json.loads(item_hashes.decode())
    else:
        item_hashes = await search_service.search_by_tags(search_params)
        await r.set(r_key, json.dumps(item_hashes), ex=5)
    
    return item_hashes