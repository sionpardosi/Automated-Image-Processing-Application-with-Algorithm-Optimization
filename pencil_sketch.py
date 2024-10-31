from PIL import Image, ImageOps, ImageFilter

def apply_pencil_sketch(image):
    # Mengonversi gambar ke grayscale
    gray_image = ImageOps.grayscale(image)
    
    # Membuat gambar blur untuk efek sketsa
    blur_image = gray_image.filter(ImageFilter.GaussianBlur(10))
    
    # Menggabungkan gambar grayscale dan blur untuk membuat efek sketsa
    pencil_sketch = Image.blend(gray_image, blur_image, 0.5)
    return pencil_sketch
