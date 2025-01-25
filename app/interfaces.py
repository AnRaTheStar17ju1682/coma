from abc import abstractmethod, ABC

from sqlalchemy.sql import Select

from PIL import Image

from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from typing import Sequence

from datetime import datetime


from models_dto import ItemPostDTO, ItemAddToDB, ItemGetDTO, ItemPutDTO, ItemUpdateInDB, ItemSearchParamsDTO, FileSavingParamsDTO

from models_orm import Base


type ItemHashStr = str


class RepositoryInterface(ABC):
    def __init__(self, engine: AsyncEngine, session_fabric: async_sessionmaker[AsyncSession]):
        self.engine = engine
        self.session_fabric = session_fabric
        super().__init__()
    
    
    @abstractmethod
    async def add_items(self, *args: tuple[ItemAddToDB, ItemHashStr]) -> list[int]:
        raise NotImplementedError
    
    
    @abstractmethod
    async def add_one_item(self, item_dto: ItemAddToDB, item_hash: str) -> int:
        raise NotImplementedError
    
    
    @abstractmethod
    async def delete_items(self, item_hashes: Sequence[str]) -> list[tuple[int, datetime]]:
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
    
    
    
    
    @abstractmethod
    def _build_tag_search_query(self, search_params: ItemSearchParamsDTO) -> Select:
        raise NotImplementedError
    
    
    @abstractmethod
    async def make_tag_search(self, query: Select) -> list:
        raise NotImplementedError


class ImageUtilsInterface(ABC):
    def __init__(self, static_salt: str):
        self.static_salt = static_salt
        super().__init__()
    
    
    @abstractmethod
    def save_to_disk(
        self,
        content_dir: str, 
        image_hash: str,
        image: Image.Image,
        thumbnail: Image.Image,
        *,
        mode: FileSavingParamsDTO
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