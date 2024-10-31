from PIL import ImageOps

def apply_invert(image):
    return ImageOps.invert(image.convert('RGB'))
