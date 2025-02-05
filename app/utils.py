from io import BytesIO

from PIL import Image

from os import remove

from glob import glob

from interfaces import ImageUtilsInterface

from config import settings


class ImageUtils(ImageUtilsInterface):
    def create_image(self, img_bytes):
        img = Image.open(BytesIO(img_bytes))
        self.salt_image(img)
        
        return img
    
    
    def save_to_disk(self, content_dir, image_hash, image, thumbnail, *, mode):
        thumbnail_path = content_dir+"/thumbnails/"+f"thumbnail_{image_hash}.webp"
        image_path = content_dir+"/"+f"{image_hash}.webp"
        
        if resize_type := mode.resize or settings.DEFAULT_RESIZE_RESOLUTION:
            if resize_type == "hd":
                new_size = (1280, 720)
            elif resize_type == "fullhd":
                new_size = (1920, 1080)
            elif resize_type == "qhd":
                new_size = (2560, 1440)
            elif resize_type == "uhd":
                new_size = (3840, 2160)
            elif settings.DEFAULT_RESIZE_RESOLUTION:
                new_size = settings.DEFAULT_RESIZE_RESOLUTION
            
            image = self.scaler(image, *new_size)
        
        
        if quality_type := mode.compress:
            if quality_type == "quality":
                quality = 85
            elif quality_type == "balance":
                quality = 75
            elif quality_type == "compact":
                quality = 65
        else:
            quality = settings.DEFAULT_IMAGES_QUALITY
            
        image.save(image_path, method=6, quality=quality)
        thumbnail.save(thumbnail_path, method=6, quality=100)
    
    
    @staticmethod
    def scaler(image, x_max=1920, y_max=1080):
        width, height = image.size
            
        if width > height:
            ratio_factor = x_max / width
            scaled_height = int(height * ratio_factor)
            new_size = (x_max, scaled_height)
            
            return image.resize(new_size, Image.Resampling.LANCZOS)
        else:
            ratio_factor = y_max / height
            scaled_width = int(width * ratio_factor)
            new_size = (scaled_width, y_max)
            
            return image.resize(new_size, Image.Resampling.LANCZOS)
    
    
    @staticmethod
    def generate_thumbnail(image):
        size = 180, 180
        thmb = image.copy()
        thmb.thumbnail(size)
        return thmb


    @staticmethod
    def salt_image(image): 
        cords = (1, 1)
        pixel = image.getpixel(cords)
        
        # sometimes a pixel is a gray grdation, not just rgb
        if isinstance(pixel, int):
            changed_pixel = pixel + 1
        elif len(pixel) == 3:
            # RGB
            changed_pixel = (pixel[0], pixel[1], pixel[2] + 1)
        elif len(pixel) == 4:
            # RGBA
            changed_pixel = (pixel[0], pixel[1], pixel[2] + 1, pixel[3])
        
        image.putpixel(cords, changed_pixel)
        
        return image

    
    @staticmethod
    def delete_image_from_disk(content_dir, image_hash):
        image_path = content_dir+"/"+f"{image_hash}"
        path_with_extension = glob(f"{image_path}.*")[0]
        remove(path_with_extension)
    
    
    @staticmethod
    def delete_thumbnail_from_disk(content_dir, image_hash):
        thumbnail_path = content_dir+"/thumbnails/"+f"thumbnail_{image_hash}"
        path_with_extension = glob(f"{thumbnail_path}.*")[0]
        remove(path_with_extension)