from sqlalchemy import select, delete, update, and_, func, not_, cast, Integer, Boolean, insert
# from sqlalchemy.orm import ...


from interfaces import RepositoryInterface

from models_orm import ItemsORM, TagsORM, ItemsTagsORM

from models_dto import ItemGetDTO


class SQLAlchemyRepository(RepositoryInterface):
    async def add_items(self, *args):
        def get_tag_type(tag, item_dto):
            for tag_type in ("tags", "characters", "copyright", "meta"):
                if tag in getattr(item_dto, tag_type):
                    return tag_type
    
        
        async def add_tags_if_not_exists(tags_and_types) -> list[TagsORM]:
            alltags = set(tag for tag, _ in tags_and_types)
            query = select(TagsORM).where(TagsORM.tag_title.in_(alltags))
            exists_tag_records = (await session.execute(query)).scalars().all()

            new_tag_records = list()
            if new_tags := alltags - {tag.tag_title for tag in exists_tag_records}:
                new_tag_records.extend([
                    TagsORM(tag_title=tag, tag_type=type)
                    for tag, type in tags_and_types
                    if tag in new_tags
                ])
                session.add_all(new_tag_records)
            
            return exists_tag_records + new_tag_records
        
        
        async with self.session_fabric() as session:
            tags_and_types = set()
            for item_dto, _ in args:
                for tag in item_dto.alltags:
                    tag_and_type = (tag, get_tag_type(tag, item_dto))
                    tags_and_types.add(tag_and_type)
            
            items = list()
            for item_dto, item_hash in args:
                item = ItemsORM(
                    item_hash=item_hash,
                **item_dto.model_dump(exclude={"tags", "characters", "copyright", "meta"})
                )
                items.append((item, item_dto))
            
            tag_records = await add_tags_if_not_exists(tags_and_types)
            session.add_all(item[0] for item in items)
            await session.flush()
            
            id_by_title = {tag.tag_title: tag.tag_id for tag in tag_records}
            
            item_ids = list()
            associations = list()
            for item, item_dto in items:
                associations.extend([
                    ItemsTagsORM(item_id=item.item_id, tag_id=id_by_title[title]) for title in item_dto.alltags
                ])
                item_ids.append(item.item_id)
            
            session.add_all(associations)
            await session.commit()
            
            return item_ids
    
    
    async def add_one_item(self, item_dto, item_hash):
        return await self.add_items((item_dto, item_hash))
    
    
    async def delete_one_item(self, item_hash, *, for_update=False):
        async with self.session_fabric() as session:
            query = (
                delete(ItemsORM)
                .where(ItemsORM.item_hash == item_hash)
                .returning(ItemsORM))
            
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
    
    
    
    
    def _build_tag_search_query(self, search_params):
        included = search_params.include_tags
        excluded = search_params.exclude_tags
        order_by = search_params.order_by.value
        conditions = list()
        
        query = select(ItemsORM.item_hash)
        
        if included or excluded:
            for include_tag in included:
                condition = func.sum(cast(TagsORM.tag_title == include_tag, Integer)) == 1
                conditions.append(condition)
            
            for exclude_tag in excluded:
                condition = func.sum(cast(TagsORM.tag_title == exclude_tag, Integer)) == 0
                conditions.append(condition)
            
            if excluded and not included:
                query = query.join_from(ItemsTagsORM, TagsORM, ItemsTagsORM.tag_id == TagsORM.tag_id)
            elif included and excluded or included:
                query = (query
                    .join_from(
                        ItemsTagsORM,
                        TagsORM,
                        and_(
                            ItemsTagsORM.tag_id == TagsORM.tag_id,
                            TagsORM.tag_title.in_(included+excluded),
                        )
                    )
                )
            query = (
                query.group_by(ItemsTagsORM.item_id, ItemsORM.item_hash, ItemsORM.score, ItemsORM.created_at)
                .having(and_(*conditions))
                .join(ItemsORM, ItemsTagsORM.item_id == ItemsORM.item_id)
            )
        else:
            query = query.distinct()
        
        query = query.limit(search_params.limit).offset(search_params.offset)
        
        if order_by == "score_asc":
            query = query.order_by(ItemsORM.score.asc())
        elif order_by == "score_desc":
            query = query.order_by(ItemsORM.score.desc())
        elif order_by == "post_date_asc":
            query = query.order_by(ItemsORM.created_at.asc())
        # order_by == "post_date_desc"
        else:
            query = query.order_by(ItemsORM.created_at.desc())
        
        return query
    
    
    async def make_tag_search(self, query) -> list:
        async with self.session_fabric() as session:
            res = await session.execute(query)
            return res.scalars().all()