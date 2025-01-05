from interfaces import RepoInterface

from database.database import seesion_factory


class SQLAlchemyRepo(RepoInterface):
    model = None
    
    
    async def add_one(image_data: ...):
        ...