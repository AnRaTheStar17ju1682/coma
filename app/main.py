from fastapi import FastAPI, UploadFile, Form, File, Depends, Header, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from aiofiles import open as async_open

from pydantic import BaseModel, StringConstraints, Field, ValidationError

from typing import Optional, Annotated, Sequence

import uvicorn


from models_dto import ItemPostDTO, Str_50, Description_350, Tags

from services.image_service import ImagesService

from dependencies import image_post_dto_dependency, image_service_dependency




app = FastAPI(title="Coma-api")




@app.get("/favicon.ico", status_code=200, response_class=FileResponse)
async def get_ico():
    return FileResponse("favicon.ico", media_type="image/x-icon", headers={"Cache-Control": "max-age=1w"})


@app.post("/images/", status_code=201)
async def upload_image(
    image: Annotated[bytes, File()],
    image_data: Annotated[ItemPostDTO, Depends(image_post_dto_dependency)],
    image_service: Annotated[ImagesService, Depends(image_service_dependency)]
):
    await image_service.post_image(image, image_data)
    return {"ok": True}


@app.get("/iamges/{name}", status_code=200, response_class=FileResponse)
async def download_image(name: str):
    file_path = f"./content/{name}"
    return FileResponse(file_path, media_type="image/jpeg")




if __name__ == "__main__":
    uvicorn.run(app, port=8000)