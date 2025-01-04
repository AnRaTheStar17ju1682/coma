from PIL import Image

from asyncio import to_thread


from interfaces import ImageUtilsInterface, RepoInterface

from models_dto import ImagePostDTO

from config import settings


content_dir = settings.CONTENT_DIR


class ImagesService():
    def __init__(
        self,
        images_repo: RepoInterface,
        image_utils: ImageUtilsInterface
    ):
        self.task_repo = images_repo
        self.image_utils = image_utils
    
    
    async def create_image(self, image_bytes: bytes, image_post_dto: ImagePostDTO) -> None:
        raw_img = self.image_utils.bytes_to_image(image_bytes)
        img = self.image_utils.get_salted_image(raw_img)
        img_hash = self.image_utils.calculate_image_hash(img)
        thumbnail = self.image_utils.generate_thumbnail(img)
        await to_thread(self.image_utils.save_to_disk, content_dir, img_hash, img, thumbnail)
        ...