from pydantic import BaseModel, Field, HttpUrl

from fastapi import Form

from typing import Optional, Annotated, Sequence


Str_50 = Annotated[Optional[str], Field(max_length=50)]
Description_350 = Annotated[Optional[str], Field(max_length=350)]
Tags = Annotated[Optional[Sequence[Str_50]], Field(max_length=100)]


class AbstractDTO(BaseModel):
    ...


class ImagePostDTO(BaseModel):
    name: Str_50 = None
    description: Description_350 = None
    
    tags: Tags = ("untagged",)
    characters: Tags = None
    copyright: Tags = None
    meta: Tags = None
    
    score: Annotated[Optional[int], Field(ge=0, le=10)] = None
    source: Annotated[Optional[HttpUrl], Field(max_length=150)] = None