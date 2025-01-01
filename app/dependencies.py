from fastapi import Form, HTTPException

from typing import Optional, Annotated

from pydantic import ValidationError

from models_dto import ImagePostDTO, Str_50, Description_350, Tags



async def image_post_dto_dependency(
    json_dump: Annotated[str | None, Form(examples=("",))] = None,
    
    
    name: Annotated[Str_50, Form()] = None,
    description: Annotated[Description_350, Form()] = None,
    tags: Tags = ("untagged",),
    meta: Annotated[Tags, Form()] = None,
    copyright: Annotated[Tags, Form()] = None,
    characters: Annotated[Tags, Form()] = None,
    score: Annotated[Optional[int], Form(ge=0, le=10)] = None,
    source: Annotated[Str_50, Form()] = None,
):
    
    if json_dump:
        try:
            return ImagePostDTO.model_validate_json(json_dump)
        except ValidationError:
            raise HTTPException(status_code=422, detail="wrong json dict")
    else:
        tags = tags[0].split(",")
        meta = meta[0].split(",")
        copyright = copyright[0].split(",")
        characters = characters[0].split(",")
        return ImagePostDTO(name=name, description=description, tags=tags, meta=meta, copyright=copyright, characters=characters, score=score, source=source)
