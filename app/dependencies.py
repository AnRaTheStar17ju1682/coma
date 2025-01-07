from fastapi import Form, HTTPException

from typing import Optional, Annotated

from pydantic import ValidationError


from config import settings

from models_dto import ItemPostDTO, Str_50, Description_350, Tags

from utils import ImageUtils

from database.repositories import SQLAlchemyRepository

from services.image_service import ImagesService


async def image_service_dependency() -> ImagesService:
    return ImagesService(repository=SQLAlchemyRepository(), image_utils=ImageUtils(settings.IMAGE_SALT))