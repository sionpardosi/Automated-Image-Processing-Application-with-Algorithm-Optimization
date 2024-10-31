from PIL import ImageFilter

def apply_sharpen(image):
    return image.filter(ImageFilter.SHARPEN)
