from abc import abstractmethod, ABC, abs

from random import Random

import hashlib

from PIL import Image




class ImageUtilsInterface(ABC):
    def __init__(self, static_salt: str):
        self.static_salt = static_salt
    
    
    @abstractmethod
    def get_dynamic_salt(self, image_hash):
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def calculate_image_hash(image):
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def determined_random_pixel(size, dynamic_salt):
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def scaler(image: Image.Image, x_max=1920, y_max=1080) -> Image.Image:
        raise NotImplementedError
    
    
    @staticmethod
    @abstractmethod
    def generate_thumbnail(image: Image.Image) -> Image.Image:
        raise NotImplementedError
    
    
    @abstractmethod
    def get_salted_image(self, image: Image.Image) -> Image:
        raise NotImplementedError




"""
# best - is a 20x space benefit and the same quality
img.save('hig.webp', method=6, quality=95)

# medium - is a 40x space benefit and a little worse quality
img.save('med.webp', method=6, quality=80)

# medium, but still acceptible quality. 70x space-savings
# most compact
img.save('worst.webp', method=6, quality=60)
"""
class ImageUtils(ImageUtilsInterface):
    def get_dynamic_salt(self, image_hash):
        return hashlib.sha256(image_hash + self.static_salt.encode())
    
    
    @staticmethod
    def calculate_image_hash(image):
        return hashlib.sha256(image.tobytes())


    @staticmethod
    def determined_random_pixel(size, dynamic_salt):
        random = Random(dynamic_salt)
        width, height = size
        random_pixel = random.randint(0, width-1), random.randint(0, height-1)
        
        return random_pixel
    
    
    @staticmethod
    def scaler(image: Image.Image, x_max=1920, y_max=1080) -> Image.Image:
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
    def generate_thumbnail(image: Image.Image) -> Image.Image:
        size = 128, 128
        thmb = image.copy()
        thmb.thumbnail(size)
        return thmb
     
     
    def get_salted_image(self, image: Image.Image) -> Image: 
        image_hash = self.calculate_image_hash(image)
        dynamic_salt = self.get_dynamic_salt(image_hash)
        
        # (x, y)
        random_pixel_location = self.determined_random_pixel(image.size, dynamic_salt)
        pixel = image.getpixel(random_pixel_location)
        changed_pixel = (pixel[0], pixel[1], pixel[2] + 1)
        image.putpixel(random_pixel_location, changed_pixel)
        
        return image