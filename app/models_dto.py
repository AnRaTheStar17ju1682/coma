from pydantic import BaseModel, Field, HttpUrl, ConfigDict, field_validator, ValidationError

from fastapi import UploadFile

from typing import Optional, Annotated, Sequence

from datetime import datetime

import re

from enum import Enum


from models_orm import TagsORM


Str_50 = Annotated[Optional[str], Field(max_length=50)]
Description_350 = Annotated[Optional[str], Field(max_length=350)]
Tags = Annotated[list[Str_50], Field(max_length=100)]


class ItemBaseDTO(BaseModel):
    name: Str_50 = None
    description: Description_350 = None
    
    tags: Tags = ["untagged"]
    characters: Tags = []
    copyright: Tags = []
    meta: Tags = []
    
    score: Optional[int] = None
    source: Optional[str] = None


class ItemPutDTO(ItemBaseDTO):
    score: Annotated[Optional[int], Field(ge=0, le=10)] = None
    source: Annotated[Optional[HttpUrl], Field(max_length=150)] = None
    
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


class ItemPostDTO(ItemPutDTO):
    file: UploadFile


class FileSavingParamsDTO(BaseModel):
    class Compress(Enum):
        """
        "quiality" - is a 20x space benefit and the same quality.
        
        "balance" - is a 40x space benefit and a little worse quality.
        
        "compact" - still acceptible quality. 70x space-savings.
        """
        quality = "quiality"
        balance = "balance"
        comapct = "compact"
    class Resize(Enum):
        hd = "hd"
        fullhd = "fullhd"
        qhd = "qhd"
        uhd = "uhd"
    
    compress: Optional[Compress] = None
    resize: Optional[Resize] = None


class ItemAddToDB(ItemBaseDTO):
    @property
    def alltags(self) -> set[str]:
        all_tags = {*self.tags, *self.characters, *self.copyright, *self.meta}
        return all_tags


class ItemUpdateInDB(ItemAddToDB):
    created_at: Optional[datetime] = None


class ItemFullDTO(ItemBaseDTO):
    item_id: int
    item_hash: str
    created_at: datetime
    updated_at: datetime
    
    @field_validator("tags", "characters", "copyright", "meta", mode="before")
    @classmethod
    def orms_to_strings(cls, value: Sequence[TagsORM]) -> list[str]:
        return [tag.tag_title for tag in value]
    
    model_config = ConfigDict(from_attributes=True)


class ItemGetDTO(ItemFullDTO):
    pass




class OrderBy(Enum):
    score_asc = "score_asc"
    score_desc = "score_desc"
    post_date_asc = "post_date_asc"
    post_date_desc = "post_date_desc"


class ItemSearchParamsDTO(BaseModel):
    order_by: OrderBy
    include_tags: list[Str_50] = []
    exclude_tags: list[Str_50] = []
    offset: int = 0
    limit: int = Field(ge=1, le=20, default=20)