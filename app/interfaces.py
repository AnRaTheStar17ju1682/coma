from abc import abstractmethod, ABC

from PIL import Image

from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


from models_dto import ItemPostDTO, ItemAddToDB, ItemGetDTO, ItemPutDTO, ItemUpdateInDB

from models_orm import Base


class RepositoryInterface(ABC):
    def __init__(self, engine: AsyncEngine, session_fabric: AsyncSession):
        self.engine = engine
        self.session_fabric = session_fabric
        super().__init__()
    
    
    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    
    
    @abstractmethod
    async def add_one_item(self, item_dto: ItemAddToDB, item_hash: str) -> int:
        raise NotImplementedError
    
    
    @abstractmethod
    async def delete_one_item(self, item_hash: str) -> int:
        raise NotImplementedError
    
    
    @abstractmethod
    async def get_item_data(self, item_hash: str) -> ItemGetDTO:
        raise NotImplementedError
    
    
    @abstractmethod
    async def update_item_data(self, item_hash: str, item_data: ItemUpdateInDB) -> int:
        raise NotImplementedError


class ImageUtilsInterface(ABC):
    def __init__(self, static_salt: str):
        self.static_salt = static_salt
        super().__init__()
    
    
    @abstractmethod
    def save_to_disk(
        content_dir: str, 
        image_hash: str,
        image: Image.Image,
        thumbnail: Image.Image,
        *,
        mode: str
    ) -> None:
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def uploadfile_to_image(image_file: UploadFile) -> Image.Image:
        raise NotImplementedError
    
    
    @abstractmethod
    def get_dynamic_salt(self, image: str) -> str:
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def calculate_image_hash(image: Image.Image) -> str:
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def determined_random_pixel(size: tuple[int, int], dynamic_salt: str) -> tuple[int, int]:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def scaler(image: Image.Image, x_max: int, y_max: int) -> Image.Image:
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def generate_thumbnail(image: Image.Image) -> Image.Image:
        raise NotImplementedError
    
    
    @abstractmethod
    def get_salted_image(self, image: Image.Image) -> Image.Image:
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def delete_image_from_disk(content_dir: str, image_hash: str) -> None:
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def delete_thumbnail_from_disk(content_dir: str, image_hash: str) -> None:
        raise NotImplementedError