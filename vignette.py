import numpy as np
from PIL import Image, ImageFilter

def apply_vignette(image, intensity=1.5):
    width, height = image.size
    x_center, y_center = width // 2, height // 2

    # Buat mask gradien melingkar untuk efek vignette
    mask = Image.new("L", (width, height), 0)
    for x in range(width):
        for y in range(height):
            dist = ((x - x_center) ** 2 + (y - y_center) ** 2) ** 0.5
            mask.putpixel((x, y), int(max(0, 255 - dist * intensity)))

    # Terapkan mask pada gambar
    image_with_vignette = Image.composite(image, Image.new("RGB", (width, height)), mask)
    return image_with_vignette
