import os
from PIL import Image

def optimize_image(input_path, output_path, target_size_kb):
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        quality = 95
        img.save(output_path, format="JPEG", quality=quality, optimize=True)

        while os.path.getsize(output_path) > target_size_kb * 1024 and quality > 10:
            quality -= 5
            img.save(output_path, format="JPEG", quality=quality, optimize=True)

        return output_path

