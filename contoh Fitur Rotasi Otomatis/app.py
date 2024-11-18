import os
from flask import Flask, render_template, request, redirect
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB file size

# Filter Gambar dengan Dynamic Programming
def apply_adaptive_contrast_filter(image):
    image = image.convert('L')  # Convert to grayscale
    pixels = np.array(image)
    height, width = pixels.shape
    
    # Apply dynamic programming to enhance contrast
    for i in range(1, height):
        for j in range(1, width):
            pixels[i, j] = max(pixels[i-1, j] + pixels[i, j], 0)
    
    # Convert numpy array back to image
    return Image.fromarray(pixels)

# Filter Gambar dengan Divide and Conquer (Edge Detection)
def apply_edge_detection_filter(image):
    image = image.convert('L')  # Convert to grayscale
    pixels = np.array(image)
    height, width = pixels.shape
    
    def detect_edges(sub_pixels):
        # Sobel filter untuk deteksi tepi
        sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        
        result = np.zeros_like(sub_pixels)
        for i in range(1, sub_pixels.shape[0] - 1):
            for j in range(1, sub_pixels.shape[1] - 1):
                gx = np.sum(sobel_x * sub_pixels[i-1:i+2, j-1:j+2])
                gy = np.sum(sobel_y * sub_pixels[i-1:i+2, j-1:j+2])
                result[i, j] = np.sqrt(gx**2 + gy**2)
        return result
    
    # Divide the image into four quadrants
    top_left = detect_edges(pixels[:height//2, :width//2])
    top_right = detect_edges(pixels[:height//2, width//2:])
    bottom_left = detect_edges(pixels[height//2:, :width//2])
    bottom_right = detect_edges(pixels[height//2:, width//2:])
    
    # Combine results
    combined_result = np.vstack([
        np.hstack([top_left, top_right]),
        np.hstack([bottom_left, bottom_right])
    ])
    
    return Image.fromarray(combined_result)

# Filter Gambar dengan Greedy Algorithm (Blur Reduction)
def apply_blur_reduction_filter(image):
    image = image.convert('RGB')
    pixels = np.array(image)
    height, width, _ = pixels.shape
    
    def select_important_area(pixels):
        # Fokus pada area tengah gambar
        center = pixels[height//4:3*height//4, width//4:3*width//4]
        return center
    
    important_area = select_important_area(pixels)
    
    # Terapkan ketajaman hanya pada area penting (Greedy)
    enhancer = ImageEnhance.Sharpness(Image.fromarray(important_area))
    sharp_important_area = enhancer.enhance(2.0)
    
    # Ganti area penting dalam gambar dengan hasil sharpen
    pixels[height//4:3*height//4, width//4:3*width//4] = np.array(sharp_important_area)
    
    return Image.fromarray(pixels)

# Filter Gambar untuk Grayscale
def apply_grayscale_filter(image):
    return image.convert('L')

# Filter Gambar untuk Sepia
def apply_sepia_filter(image):
    pixels = np.array(image)
    tr = [0.393, 0.769, 0.189]
    tg = [0.349, 0.686, 0.168]
    tb = [0.272, 0.534, 0.131]
    
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            r, g, b = pixels[i][j]
            pixels[i][j] = [min(255, int(r * tr[0] + g * tg[0] + b * tb[0])),
                            min(255, int(r * tr[1] + g * tg[1] + b * tb[1])),
                            min(255, int(r * tr[2] + g * tg[2] + b * tb[2]))]
    return Image.fromarray(pixels)

# Fungsi untuk menangani file upload dan filter
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        # Simpan gambar yang diupload
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Baca gambar
        image = Image.open(file_path)
        
        # Ambil filter yang dipilih
        filter_type = request.form.get('filter')

        if filter_type == 'grayscale':
            filtered_image = apply_grayscale_filter(image)
        elif filter_type == 'sepia':
            filtered_image = apply_sepia_filter(image)
        elif filter_type == 'adaptive_contrast':
            filtered_image = apply_adaptive_contrast_filter(image)
        elif filter_type == 'edge_detection':
            filtered_image = apply_edge_detection_filter(image)
        elif filter_type == 'blur_reduction':
            filtered_image = apply_blur_reduction_filter(image)
        else:
            filtered_image = apply_grayscale_filter(image)

        # Simpan gambar yang telah difilter
        filtered_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'filtered_' + filename)
        filtered_image.save(filtered_image_path)

        return render_template('index.html', uploaded_image=file_path, filtered_image=filtered_image_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
