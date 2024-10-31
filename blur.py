from PIL import ImageFilter

def apply_blur(image):
    return image.filter(ImageFilter.GaussianBlur(5))
