from PIL import Image, ImageFilter, ImageEnhance

def apply_cartoon(image):
    # Reduksi warna untuk efek kartun
    image = image.convert("RGB")
    image = image.filter(ImageFilter.ModeFilter(size=9))
    image = ImageEnhance.Color(image).enhance(2)  # Warna lebih hidup
    # Tambahkan edge untuk kontur yang jelas
    edges = image.filter(ImageFilter.FIND_EDGES)
    image.paste(edges)
    return image
