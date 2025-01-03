from typing import Type, Annotated


from utils import ImageUtilsInterface


class ImagesService():
    def __init__(
        self,
        images_repo: Type,
        image_utils: ImageUtilsInterface
    ):
        self.task_repo = images_repo
        self.image_utils = image_utils