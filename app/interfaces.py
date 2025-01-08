from abc import abstractmethod, ABC

from PIL import Image

from fastapi import UploadFile


from models_dto import ItemPostDTO, ItemAddToDB




class RepositoryInterface(ABC):
    @staticmethod
    @abstractmethod
    async def add_one_item(item_dto: ItemAddToDB, item_hash: str):
        raise NotImplementedError


class ImageUtilsInterface(ABC):
    def __init__(self, static_salt: str):
        self.static_salt = static_salt
    
    
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