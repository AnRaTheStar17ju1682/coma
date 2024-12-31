from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

from aiofiles import open as async_open

from pydantic import BaseModel, StringConstraints, Field, constr, con

from typing import Optional, Annotated, Sequence

import uvicorn


app = FastAPI(title="Coma-api")


Name = Annotated[str, Field(max_length=50)]
Description_350 = Annotated[str, Field(max_length=350)]
Tags = Annotated[Sequence[constr(max_length=50)], Field(max_length=100)]


class ImagePost(BaseModel):
    name: Optional[Name] = None
    description: Description_350
    
    tags: Tags = ("untagged")
    meta: Optional[Tags] = None
    copyright: Optional[Tags] = None
    characters: Optional[Tags] = None
    
    score: Annotated[int, Field(ge=0, le=10)]
    source: Annotated[Optional[str], Field(max_length=50)] = None


@app.get("/favicon.ico", status_code=200, response_class=FileResponse)
async def get_ico():
    return FileResponse("favicon.ico", media_type="image/x-icon", headers={"Cache-Control": "max-age=1w"})


@app.post("/images/{name}", status_code=201)
async def upload_image(name: str, image: UploadFile):
    async with async_open(file=f"./content/{name}", mode="wb") as file:
        await file.write(await image.read())
    return {"ok": True}


@app.get("/iamges/{name}", status_code=200, response_class=FileResponse)
async def download_image(name: str):
    file_path = f"./content/{name}"
    return FileResponse(file_path, media_type="image/jpeg")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)