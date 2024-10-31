from PIL import Image

def apply_black_white(image):
    return image.convert('L')
