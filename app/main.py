from fastapi import FastAPI, UploadFile, Form, File, Depends, Header, HTTPException
from fastapi.responses import FileResponse

from aiofiles import open as async_open

from pydantic import BaseModel, StringConstraints, Field, ValidationError

from typing import Optional, Annotated, Sequence

import uvicorn


from models_dto import ImagePostDTO, Str_50, Description_350, Tags

from dependencies import image_post_dto_dependency




app = FastAPI(title="Coma-api")




@app.get("/favicon.ico", status_code=200, response_class=FileResponse)
async def get_ico():
    return FileResponse("favicon.ico", media_type="image/x-icon", headers={"Cache-Control": "max-age=1w"})


@app.post("/images/", status_code=201)
async def upload_image(image: UploadFile, image_data: Annotated[ImagePostDTO, Depends(image_post_dto_dependency)]):
    async with async_open(file=f"./content/{image.filename}", mode="wb") as file:
       await file.write(await image.read())
    return image_data
    # return {"ok": True}


@app.get("/iamges/{name}", status_code=200, response_class=FileResponse)
async def download_image(name: str):
    file_path = f"./content/{name}"
    return FileResponse(file_path, media_type="image/jpeg")




if __name__ == "__main__":
    uvicorn.run(app, port=8000)