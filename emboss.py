from PIL import ImageFilter

def apply_emboss(image):
    return image.filter(ImageFilter.EMBOSS)
