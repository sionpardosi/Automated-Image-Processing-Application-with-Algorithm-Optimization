
import os
from PIL import Image
from black_white import apply_black_white
from blur import apply_blur
from invert import apply_invert
from sepia import apply_sepia
from emboss import apply_emboss
from sharpen import apply_sharpen
from brighten import apply_brighten
from vignette import apply_vignette
from cartoon import apply_cartoon
from glow import apply_glow
from hdr import apply_hdr
from pencil_sketch import apply_pencil_sketch
from glow import apply_glow

def apply_effect(image, effect):
    if effect == 'black_white':
        return apply_black_white(image)
    elif effect == 'blur':
        return apply_blur(image)
    elif effect == 'invert':
        return apply_invert(image)
    elif effect == 'sepia':
        return apply_sepia(image)
    elif effect == 'emboss':
        return apply_emboss(image)
    elif effect == 'sharpen':
        return apply_sharpen(image)
    elif effect == 'brighten':
        return apply_brighten(image)
    elif effect == 'vignette':
        return apply_vignette(image)
    elif effect == 'cartoon':
        return apply_cartoon(image)
    elif effect == 'glow':  # Tambahkan efek glow di sini
        return apply_glow(image)
    elif effect == 'hdr':
        return apply_hdr(image)
    elif effect == 'pencil_sketch':
        return apply_pencil_sketch(image)
    else:
        raise ValueError("Effect not supported")


def process_image(upload, effect):
    img = Image.open(upload)
    processed_image = apply_effect(img, effect)
    
    # Tentukan jalur penyimpanan gambar hasil
    result_dir = 'static'
    result_path = os.path.join(result_dir, 'processed_image.jpg')
    
    # Buat direktori jika belum ada
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    # Simpan gambar
    processed_image.save(result_path)
    
    return result_path




