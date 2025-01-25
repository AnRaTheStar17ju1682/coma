from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from config import settings


content_path = settings.CONTENT_DIR
router = APIRouter(prefix="/files", tags=["files"])


def return_if_exists(file_path: str):
    file_path = Path(file_path)
    
    if file_path.exists():
        return FileResponse(file_path, media_type="image/webp")  
    else:
        raise HTTPException(status_code=404, detail="File not found")


@router.get("/item/{item_hash}", status_code=200, response_class=FileResponse)
async def download_item(item_hash: str):
    file_path = f"{content_path}/{item_hash}.webp"
    return return_if_exists(file_path)


@router.get("/thumbnail/{item_hash}", status_code=200, response_class=FileResponse)
async def download_thumbnail(item_hash: str):
    file_path = f"{content_path}/thumbnails/thumbnail_{item_hash}.webp"
    return return_if_exists(file_path)