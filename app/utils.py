from random import Random

import hashlib

from PIL import Image


from interfaces import ImageUtilsInterface


class ImageUtils(ImageUtilsInterface):
    @staticmethod
    def save_to_disk(content_dir, image_hash, image, thumbnail, *, mode="balance"):
        """
        args for mode:
        
        "quiality" - is a 20x space benefit and the same quality.
        
        "balance" - is a 40x space benefit and a little worse quality.
        
        "compact" - still acceptible quality. 70x space-savings.
        """
        if not mode in ('quiality', 'balance', 'compact'):
            raise ValueError(f"Invalid mode: {mode}. Expected one of: 'quiality', 'balance', 'compact'")
        
        thumbnail_path = content_dir+"/thumbnails/"+f"thumbnail_{image_hash}.webp"
        image_path = content_dir+"/"+f"{image_hash}.webp"
        
        thumbnail.save(thumbnail_path, method=6)
        
        if mode == "quiality":
            image.save(image_path, method=6, quality=95)
        elif mode == "balance":
            image.save(image_path, method=6, quality=90)
        elif mode == "compact":
            image.save(image_path, method=6)
    
    
    @staticmethod
    def bytes_to_image(image_bytes):
        return Image.open(image_bytes)

    
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