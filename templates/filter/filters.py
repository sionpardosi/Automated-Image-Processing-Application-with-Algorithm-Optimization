from PIL import Image, ImageFilter, ImageOps

def blur_divide_and_conquer(img):
    """Fungsi untuk menerapkan efek blur pada gambar."""
    return img.filter(ImageFilter.BLUR)

def grayscale_iterative(img):
    """Fungsi untuk mengubah gambar menjadi grayscale secara iteratif."""
    return img.convert("L").convert("RGB")

def sharpen_divide_and_conquer(img):
    """Fungsi untuk mengasah gambar."""
    return img.filter(ImageFilter.SHARPEN)

def sepia_iterative(img):
    """Fungsi untuk mengubah gambar menjadi efek sepia."""
    width, height = img.size
    pixels = img.load()  # Membaca data pixel
    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > 255:
                tr = 255

            if tg > 255:
                tg = 255

            if tb > 255:
                tb = 255

            pixels[px, py] = (tr,tg,tb)

    return img

def edge_detection_dp(img):
    """Fungsi untuk mendeteksi tepi menggunakan filter."""
    return img.filter(ImageFilter.FIND_EDGES)

def selective_filter_backtracking(img, target_color, replacement_color):
    """Fungsi untuk menerapkan filter selektif berdasarkan warna tertentu."""
    width, height = img.size
    pixels = img.load()
    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))

            # Filter berdasarkan warna tertentu (misalnya, mengganti warna biru dengan merah)
            if (r, g, b) == target_color:
                pixels[px, py] = replacement_color

    return img
