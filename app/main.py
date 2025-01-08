from fastapi import FastAPI, UploadFile, Form, File, Depends, Header, HTTPException, BackgroundTasks, status
from fastapi.responses import FileResponse

from sqlalchemy.exc import IntegrityError, NoResultFound

from psycopg.errors import UniqueViolation

from pydantic import BaseModel, StringConstraints, Field, ValidationError

from typing import Optional, Annotated, Sequence

import uvicorn


from models_dto import ItemPostDTO, Str_50, Description_350, Tags

from services.image_service import ImagesService

from dependencies import image_service_dependency




app = FastAPI(title="Coma-api")




@app.get("/favicon.ico", status_code=200, response_class=FileResponse)
async def get_ico():
    return FileResponse("favicon.ico", media_type="image/x-icon", headers={"Cache-Control": "max-age=1w"})


@app.post("/items/", status_code=201)
async def upload_item(
    item: Annotated[ItemPostDTO, Form()],
    image_service: Annotated[ImagesService, Depends(image_service_dependency)]
):
    try:
        item_hash, item_id = await image_service.post_image(image=item)
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
    return {"item_hash": item_hash, "created_item_id": item_id}


@app.delete("/items/{item_hash}", status_code=200)
async def delete_item(
    item_hash: str,
    image_service: Annotated[ImagesService, Depends(image_service_dependency)]
):
    try:
        deleted_item_id = await image_service.delete_from_disk(image_hash=item_hash)
        
        return {"succes": True, "deleted_item_hash": item_hash, "deleted_item_id": deleted_item_id}
    except NoResultFound as err:
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "An Item with this hash does not exists",
                "hash": item_hash
            }
        )
        


@app.get("/items/{item_hash}", status_code=200, response_class=FileResponse)
async def download_item(item_hash: str):
    file_path = f"./content/{item_hash}"
    return FileResponse(file_path)# , media_type="image/jpeg")




if __name__ == "__main__":
    uvicorn.run(app, port=8000)