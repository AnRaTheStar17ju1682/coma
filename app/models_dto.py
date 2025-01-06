from pydantic import BaseModel, Field, HttpUrl, ConfigDict, field_validator, computed_field

from fastapi import Form

from typing import Optional, Annotated, Sequence


from models_orm import TagsORM


Str_50 = Annotated[Optional[str], Field(max_length=50)]
Description_350 = Annotated[Optional[str], Field(max_length=350)]
Tags = Annotated[Optional[list[Str_50]], Field(max_length=100)]


class AbstractDTO(BaseModel):
    ...


class ItemBaseDTO(BaseModel):
    name: Str_50 = None
    description: Description_350 = None
    
    tags: Tags = ("untagged",)
    characters: Tags = None
    copyright: Tags = None
    meta: Tags = None
    
    score: Annotated[Optional[int], Field(ge=0, le=10)] = None
    source: Annotated[Optional[HttpUrl], Field(max_length=150)] = None
    
    @property
    def alltags(self) -> set[str]:
        all_tags = {*self.tags, *self.characters, *self.copyright, *self.meta}
        return all_tags
    
    @field_validator("source", mode="after")
    @classmethod
    def http_to_string(cls, value: HttpUrl) -> list[str]:
        return value.unicode_string()


class ItemPostDTO(ItemBaseDTO):
    pass


class ItemFullDTO(ItemBaseDTO):
    item_id: int
    item_hash: str
    
    @field_validator("tags", "characters", "copyright", "meta", mode="before")
    @classmethod
    def orms_to_strings(cls, value: Sequence[TagsORM]) -> list[str]:
        return [tag.tag_title for tag in value]
    
    model_config = ConfigDict(from_attributes=True)