from interfaces import RepoInterface

from database.database import seesion_factory


from models_dto import ItemPostDTO

from models_orm import ItemsORM, TagsORM, ItemsTagsORM


class SQLAlchemyRepo(RepoInterface):
    async def add_one_item(image_data: ItemPostDTO):
        async with seesion_factory() as session
        ...