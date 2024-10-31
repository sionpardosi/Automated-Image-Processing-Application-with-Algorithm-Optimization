from PIL import Image

def apply_sepia(image):
    sepia_image = Image.new("RGB", image.size)
    pixels = image.load()
    sepia_pixels = sepia_image.load()
    
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            r, g, b = pixels[x, y]
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            sepia_pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))
    
    return sepia_image
