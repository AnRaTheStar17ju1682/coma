from pydantic import BaseModel, Field, HttpUrl, ConfigDict, field_validator, ValidationError

from fastapi import UploadFile

from typing import Optional, Annotated, Sequence

from datetime import datetime

import re


from models_orm import TagsORM


Str_50 = Annotated[Optional[str], Field(max_length=50)]
Description_350 = Annotated[Optional[str], Field(max_length=350)]
Tags = Annotated[Optional[list[Str_50]], Field(max_length=100)]


class AbstractDTO(BaseModel):
    ...


class ItemBaseDTO(BaseModel):
    name: Str_50 = None
    description: Description_350 = None
    
    tags: Tags = ["untagged"]
    characters: Tags = []
    copyright: Tags = []
    meta: Tags = []
    
    score: Annotated[Optional[int], Field(ge=0, le=10)] = None
    source: Annotated[Optional[HttpUrl], Field(max_length=150)] = None


class ItemPostDTO(ItemBaseDTO):
    file: UploadFile
    
    @field_validator("tags", "characters", "copyright", "meta", mode="after")
    @classmethod
    def tags_is_alphanumeric_and_underscore(cls, value: list[str]) -> list[str]:
        pattern = r"^\w+$"

        for item in value:
            if not re.match(pattern, item):
                raise ValueError(
                    f"Alphanumeric violation in '{item}'. Only alphanumeric and underscores are allowed."
                )
        return value
    
    
    @field_validator("source", mode="after")
    @classmethod
    def http_to_string(cls, value: HttpUrl) -> str:
        return value.unicode_string()


class ItemAddToDB(ItemBaseDTO):
    @property
    def alltags(self) -> set[str]:
        all_tags = {*self.tags, *self.characters, *self.copyright, *self.meta}
        return all_tags


class ItemFullDTO(ItemBaseDTO):
    item_id: int
    item_hash: str
    created_at: datetime
    created_at: datetime
    
    @field_validator("tags", "characters", "copyright", "meta", mode="before")
    @classmethod
    def orms_to_strings(cls, value: Sequence[TagsORM]) -> list[str]:
        return [tag.tag_title for tag in value]
    
    model_config = ConfigDict(from_attributes=True)


class ItemGetDTO(ItemFullDTO):
    pass