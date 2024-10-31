from PIL import ImageEnhance, ImageFilter

def apply_hdr(image):
    # Tingkatkan kontras dan detail
    contrast = ImageEnhance.Contrast(image).enhance(1.5)
    detail = contrast.filter(ImageFilter.DETAIL)
    return detail
