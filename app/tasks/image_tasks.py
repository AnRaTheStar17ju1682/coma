from celery.utils.log import get_task_logger

from _celery import celery_app

from utils import ImageUtils

from models_dto import FileSavingParamsDTO

from config import settings


content_dir = settings.CONTENT_DIR
img_utils = ImageUtils(settings.IMAGE_SALT)
logger = get_task_logger(__name__)


@celery_app.task(name="image_tasks.process_image")
def process_image(img_bytes: bytes, img_hash: str, mode: str):
    mode = FileSavingParamsDTO.model_validate_json(mode)
    print(mode, type(mode))
    img = img_utils.create_image(img_bytes)
    thumbnail = img_utils.generate_thumbnail(img)
    img_utils.save_to_disk(content_dir, img_hash, img, thumbnail, mode=mode)
    
    logger.info("%s saved to a disk", img_hash)