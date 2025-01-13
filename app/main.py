from fastapi import FastAPI, UploadFile, Form, File, Depends, Header, HTTPException, BackgroundTasks, status, Body
from fastapi.responses import FileResponse

from sqlalchemy.exc import IntegrityError, NoResultFound

from psycopg.errors import UniqueViolation

from pydantic import BaseModel, StringConstraints, Field, ValidationError

from typing import Optional, Annotated, Sequence

import uvicorn


from models_dto import ItemPostDTO, ItemPutDTO, Str_50, Description_350, Tags, ItemSearchParamsDTO

from services.image_service import ImagesService
from services.search_service import SearchService

from dependencies import image_service_dependency, search_service_dependency




app = FastAPI(title="Coma-api")




@app.get("/favicon.ico", status_code=200, response_class=FileResponse)
async def get_ico():
    return FileResponse("favicon.ico", media_type="image/x-icon", headers={"Cache-Control": "max-age=1w"})


@app.post("/items/", status_code=201, tags=["item_endpoints"])
async def upload_item(
    item: Annotated[ItemPostDTO, Form()],
    image_service: Annotated[ImagesService, Depends(image_service_dependency)],
    background_tasks: BackgroundTasks
):
    try:
        item_hash, item_id = await image_service.post_image(image=item, background_tasks=background_tasks)
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


@app.delete("/items/{item_hash}", status_code=200, tags=["item_endpoints"])
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


@app.get("/items/{item_hash}", status_code=200, tags=["item_endpoints"])
async def get_item_data(
    item_hash: str,
    image_service: Annotated[ImagesService, Depends(image_service_dependency)]
):
    try:
        item_data = await image_service.get_image_data(image_hash=item_hash)
        
        return item_data
    except NoResultFound as err:
        raise HTTPException(
            status_code=404,
            detail={
                "msg": "An Item with this hash does not exists",
                "hash": item_hash
            }
        )


@app.put("/items/{item_hash}", status_code=200, tags=["item_endpoints"])
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


@app.post("/tag_search/", tags=["search"])
async def tag_search(
    search_params: ItemSearchParamsDTO,
    search_service: Annotated[SearchService, Depends(search_service_dependency)]
) -> list[str]:
    item_hashes = await search_service.search_by_tags(search_params)
    return item_hashes




if __name__ == "__main__":
    uvicorn.run(app, port=8000)