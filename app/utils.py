from random import Random

import hashlib

from PIL import Image

from os import remove

from glob import glob


from interfaces import ImageUtilsInterface

from config import settings


class ImageUtils(ImageUtilsInterface):
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
            if quality_type == "quiality":
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
    def uploadfile_to_image(image_file):
        return Image.open(image_file.file)

    
    def get_dynamic_salt(self, image_hash: str):
        string = image_hash + self.static_salt
        dynamic_salt = hashlib.sha256(string.encode())
        return dynamic_salt.hexdigest()
    
    
    @staticmethod
    def calculate_image_hash(image):
        hash = hashlib.sha256(image.tobytes())
        return hash.hexdigest()


    @staticmethod
    def determined_random_pixel(size, dynamic_salt):
        random = Random(dynamic_salt)
        width, height = size
        random_pixel = random.randint(0, width-1), random.randint(0, height-1)
        
        return random_pixel
    
    
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
        size = 128, 128
        thmb = image.copy()
        thmb.thumbnail(size)
        return thmb
     
     
    def get_salted_image(self, image): 
        image_hash = self.calculate_image_hash(image)
        dynamic_salt = self.get_dynamic_salt(image_hash)
        
        # (x, y)
        random_pixel_location = self.determined_random_pixel(image.size, dynamic_salt)
        pixel = image.getpixel(random_pixel_location)
        changed_pixel = (pixel[0], pixel[1], pixel[2] + 1)
        image.putpixel(random_pixel_location, changed_pixel)
        
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