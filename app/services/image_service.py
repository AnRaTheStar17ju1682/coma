from PIL import Image

from asyncio import to_thread

from fastapi import BackgroundTasks


from interfaces import ImageUtilsInterface, RepositoryInterface

from models_dto import ItemPostDTO, ItemAddToDB, ItemGetDTO, ItemPutDTO, ItemUpdateInDB, FileSavingParamsDTO

from config import settings


content_dir = settings.CONTENT_DIR


class ImagesService():
    def __init__(
        self,
        repository: RepositoryInterface,
        image_utils: ImageUtilsInterface
    ):
        self.repository = repository
        self.image_utils = image_utils
    
    
    async def post_image(
        self,
        image: ItemPostDTO,
        background_tasks: BackgroundTasks,
        save_mode: FileSavingParamsDTO
    ) -> tuple[str, int]:
        image_model_for_db = ItemAddToDB.model_validate(image.model_dump(exclude={"file"}, exclude_unset=True))
        raw_img = self.image_utils.uploadfile_to_image(image.file)
        img = self.image_utils.get_salted_image(raw_img)
        img_hash = self.image_utils.calculate_image_hash(img)
        thumbnail = self.image_utils.generate_thumbnail(img)
        
        created_item_id = await self.repository.add_one_item(image_model_for_db, img_hash)
        background_tasks.add_task(
            self.image_utils.save_to_disk,
            content_dir, img_hash, img, thumbnail,
            mode=save_mode
        )
        
        return img_hash, created_item_id
    
    
    async def delete_from_disk(self, image_hash: str) -> int:
        deleted_item_id = await self.repository.delete_one_item(image_hash)
        self.image_utils.delete_image_from_disk(content_dir, image_hash)
        self.image_utils.delete_thumbnail_from_disk(content_dir, image_hash)
        
        return deleted_item_id
    
    
    async def get_image_data(self, image_hash: str) -> ItemGetDTO:
        image_data = await self.repository.get_item_data(image_hash)
        
        return image_data
    
    
    async def update_image_data(self, image_hash: str, image_dto: ItemPutDTO):
        image_dto_db = ItemUpdateInDB.model_validate(image_dto.model_dump())
        
        item_new_id = await self.repository.update_item_data(image_hash, image_dto_db)
        
        return item_new_id