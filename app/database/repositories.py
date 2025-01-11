from sqlalchemy import select, delete, update
# from sqlalchemy.orm import ...


from interfaces import RepositoryInterface

from models_orm import ItemsORM, TagsORM, ItemsTagsORM

from models_dto import ItemGetDTO


class SQLAlchemyRepository(RepositoryInterface):
    async def add_one_item(self, item_dto, item_hash):
        def get_tag_type(tag):
            for tag_type in ("tags", "characters", "copyright", "meta"):
                if tag in getattr(item_dto, tag_type):
                    return tag_type
        
        async with self.session_fabric() as session:
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
            else:
                new_tag_records = list()
            
            session.add(item)
            await session.flush()
            
            item_id = item.item_id
            all_tag_records = tag_records + new_tag_records
            tag_ids = (tag.tag_id for tag in all_tag_records)
            associations = (
                ItemsTagsORM(item_id=item_id, tag_id=tag_id) for tag_id in tag_ids
            )
            session.add_all(associations)
            await session.commit()
            
            return item_id
    
    
    async def delete_one_item(self, item_hash, *, for_update=False):
        async with self.session_fabric() as session:
            query = (delete(ItemsORM).
                where(ItemsORM.item_hash == item_hash).
                returning(ItemsORM))
            
            result = await session.execute(query)
            item = result.scalar_one()
            deleted_item_id, creation_date = item.item_id, item.created_at
            await session.commit()
            
            if for_update:
                return creation_date
            else:
                return deleted_item_id
    
    
    async def get_item_data(self, item_hash):
        async with self.session_fabric() as session:
            query = select(ItemsORM).where(ItemsORM.item_hash == item_hash)
            
            result = await session.execute(query)
            item = result.scalar_one()
            item_dto = ItemGetDTO.model_validate(item)
            
            return(item_dto)
    
    
    async def update_item_data(self,  item_hash, item_data):
        creation_date = await self.delete_one_item(item_hash, for_update=True)
        
        item_data.created_at = creation_date
        
        updated_item_new_id = await self.add_one_item(item_data, item_hash)
        
        return updated_item_new_id