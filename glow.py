from PIL import ImageEnhance, ImageFilter

def apply_glow(image, brightness=1.2, blur_radius=5):
    # Meningkatkan kecerahan gambar
    enhancer = ImageEnhance.Brightness(image)
    bright_image = enhancer.enhance(brightness)
    
    # Menambahkan efek blur pada gambar
    glow_image = bright_image.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Menggabungkan gambar asli dan gambar dengan efek glow
    combined_image = Image.blend(image, glow_image, 0.5)
    
    return combined_image
