from PIL import ImageEnhance

def apply_brighten(image, factor=1.5):
    # Meningkatkan kecerahan gambar
    enhancer = ImageEnhance.Brightness(image)
    bright_image = enhancer.enhance(factor)
    return bright_image
