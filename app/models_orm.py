from sqlalchemy import ForeignKey, and_, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Annotated, Optional

from enum import Enum

from datetime import datetime


from database.database import Base


int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
rel_kw_taglike = {
    "primaryjoin": "ItemsORM.item_id == ItemsTagsORM.item_id",
    "lazy": "selectin",
    "back_populates": "tag_items",
    "secondary": "items_tags",
    "viewonly": True
}


class TagType(Enum):
    tags = "tags"
    characters = "characters"
    copyright = "copyright"
    meta = "meta"


class ItemsORM(Base):
    __tablename__ = "items"
    
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    
    tags: Mapped[list["TagsORM"]] = relationship(
        secondaryjoin="and_(ItemsTagsORM.tag_id == TagsORM.tag_id, TagsORM.tag_type == 'tags')",
        **rel_kw_taglike
    )
    characters: Mapped[list["TagsORM"]] = relationship(
        secondaryjoin="and_(ItemsTagsORM.tag_id == TagsORM.tag_id, TagsORM.tag_type == 'characters')",
        **rel_kw_taglike
    )
    copyright: Mapped[list["TagsORM"]] = relationship(
        secondaryjoin="and_(ItemsTagsORM.tag_id == TagsORM.tag_id, TagsORM.tag_type == 'copyright')",
        **rel_kw_taglike
    )
    meta: Mapped[list["TagsORM"]] = relationship(
        secondaryjoin="and_(ItemsTagsORM.tag_id == TagsORM.tag_id, TagsORM.tag_type == 'meta')",
        **rel_kw_taglike
    )
    
    score: Mapped[Optional[int]] # have index
    source: Mapped[Optional[str]]
    
    # new attrs compared PostDTO model
    item_id: Mapped[int_pk]
    item_hash: Mapped[str] = mapped_column(index=True, unique=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    
    __table_args__ = (
        Index("ix_score_not_null", "score", postgresql_where="score IS NOT NULL"),
    )


class TagsORM(Base):
    __tablename__ = "tags"
    
    tag_id: Mapped[int_pk]
    tag_title: Mapped[str] = mapped_column(index=True, unique=True)
    tag_type: Mapped[TagType] = mapped_column(index=True)
    
    tag_items: Mapped[list["ItemsORM"]] = relationship(
        secondary="items_tags",
        lazy="selectin",
    )


class ItemsTagsORM(Base):
    __tablename__ = "items_tags"
    
    item_id: Mapped[int] = mapped_column(ForeignKey("items.item_id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)