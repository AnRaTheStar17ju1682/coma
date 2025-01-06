from PIL import Image

from asyncio import to_thread


from interfaces import ImageUtilsInterface, RepositoryInterface

from models_dto import ItemPostDTO

from config import settings


content_dir = settings.CONTENT_DIR
quality = settings.DEFAULT_IMAGES_QUALITY


class ImagesService():
    def __init__(
        self,
        repository: RepositoryInterface,
        image_utils: ImageUtilsInterface
    ):
        self.repository = repository
        self.image_utils = image_utils
    
    
    async def post_image(self, image_bytes: bytes, item_post_dto: ItemPostDTO) -> None:
        raw_img = self.image_utils.bytes_to_image(image_bytes)
        img = self.image_utils.get_salted_image(raw_img)
        img_hash = self.image_utils.calculate_image_hash(img)
        thumbnail = self.image_utils.generate_thumbnail(img)
        await to_thread(self.image_utils.save_to_disk, content_dir, img_hash, img, thumbnail, mode=quality)
        
        await self.repository.add_one_item(item_post_dto, img_hash)