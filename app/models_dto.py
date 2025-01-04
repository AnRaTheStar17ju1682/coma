from pydantic import BaseModel, StringConstraints, Field, constr

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
    meta: Tags = None
    copyright: Tags = None
    characters: Tags = None
    
    score: Annotated[Optional[int], Field(ge=0, le=10)] = None
    source: Str_50 = None