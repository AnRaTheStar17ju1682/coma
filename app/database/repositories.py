from sqlalchemy import select
# from sqlalchemy.orm import ...


from interfaces import RepositoryInterface

from database.database import session_factory

from models_dto import ItemPostDTO

from models_orm import ItemsORM, TagsORM, ItemsTagsORM


class SQLAlchemyRepository(RepositoryInterface):
    @staticmethod
    async def add_one_item(item_dto, item_hash):
        def get_tag_type(tag):
            for tag_type in ("tags", "characters", "copyright", "meta"):
                if tag in getattr(item_dto, tag_type):
                    return tag_type
        
        async with session_factory() as session:
            item = ItemsORM(
                item_hash=item_hash,
               **item_dto.model_dump(exclude={"tags", "characters", "copyright", "meta"})
            )

            query = select(TagsORM).where(TagsORM.tag_title.in_(item_dto.alltags))
            tag_records = (await session.execute(query)).scalars().all()
            
            if new_tags := item_dto.alltags - {tag.tag_title for tag in tag_records}:
                new_tag_records = [TagsORM(tag_title=tag, tag_type=get_tag_type(tag)) for tag in new_tags]
                session.add_all(
                    new_tag_records
                )
            
            session.add(item)
            await session.flush()
            
            all_tag_records = tag_records + new_tag_records
            tag_ids = (tag.tag_id for tag in all_tag_records)
            associations = (
                ItemsTagsORM(item_id=item.item_id, tag_id=tag_id) for tag_id in tag_ids
            )
            session.add_all(associations)
            await session.commit()