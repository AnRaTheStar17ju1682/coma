from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(prefix="/files", tags=["files"])


@router.get("/item/{item_hash}", status_code=200, response_class=FileResponse)
async def download_item(item_hash: str):
    file_path = f"./content/{item_hash}.webp"
    return FileResponse(file_path, media_type="image/webp")


@router.get("/thumbnail/{item_hash}", status_code=200, response_class=FileResponse)
async def download_thumbnail(item_hash: str):
    file_path = f"./content/thumbnails/thumbnail_{item_hash}.webp"
    return FileResponse(file_path, media_type="image/webp")