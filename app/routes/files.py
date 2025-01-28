from pathlib import Path

from typing import Annotated

import anyio.to_process
import anyio.to_thread
from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.responses import FileResponse

from redis.asyncio import Redis

import anyio

from config import settings

from routes.dependencies import redis_files_dependency


content_path = settings.CONTENT_DIR
router = APIRouter(prefix="/files", tags=["files"])


async def get_file_if_exists(file_path: str):
    file_path = Path(file_path)
    
    # "image/webp"
    if exists := await anyio.to_thread.run_sync(file_path.exists):
        async with await anyio.open_file(file_path, mode="rb") as file:
            file_bytes = await file.read()
        
        return file_bytes
    else:
        return None


async def cached_get_file_if_exists(file_path, r: Redis):
    if item_bytes := await r.get(file_path):
        pass
    elif item_bytes := await get_file_if_exists(file_path):
        await r.set(file_path, item_bytes)
    else:
        item_bytes = None
    
    return item_bytes


@router.get("/item/{item_hash}", status_code=200)
async def download_item(item_hash: str, r: Annotated[Redis, Depends(redis_files_dependency)]):
    file_path = f"{content_path}/{item_hash}.webp"
    
    if file_bytes := await cached_get_file_if_exists(file_path, r):
        return Response(file_bytes, media_type="image/webp")
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.get("/thumbnail/{item_hash}", status_code=200)
async def download_thumbnail(item_hash: str, r: Annotated[Redis, Depends(redis_files_dependency)]):
    file_path = f"{content_path}/thumbnails/thumbnail_{item_hash}.webp"

    if file_bytes := await cached_get_file_if_exists(file_path, r):
        return Response(file_bytes, media_type="image/webp")
    else:
        raise HTTPException(status_code=404, detail="Thumbnail not found")