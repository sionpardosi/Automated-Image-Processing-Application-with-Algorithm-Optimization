from flask import Flask, render_template, request, send_from_directory
import os
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

# Folder untuk menyimpan gambar yang di-upload
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fungsi untuk menerapkan Gaussian Blur dengan Divide and Conquer
def gaussian_blur(image, kernel_size=5, sigma=1.0):
    kernel = np.fromfunction(
        lambda x, y: (1/ (2 * np.pi * sigma ** 2)) * np.exp(
            - ((x - (kernel_size - 1) / 2) ** 2 + (y - (kernel_size - 1) / 2) ** 2) / (2 * sigma ** 2)),
        (kernel_size, kernel_size)
    )
    kernel /= np.sum(kernel)
    
    def divide_and_conquer(img):
        h, w = img.shape
        mid_h, mid_w = h // 2, w // 2
        parts = [img[:mid_h, :mid_w], img[:mid_h, mid_w:], img[mid_h:, :mid_w], img[mid_h:, mid_w:]]
        return parts

    def process_parts(parts):
        blurred_parts = []
        for part in parts:
            blurred_part = apply_gaussian_kernel(part, kernel)
            blurred_parts.append(blurred_part)
        return blurred_parts

    def merge_parts(parts):
        top_half = np.concatenate((parts[0], parts[1]), axis=1)
        bottom_half = np.concatenate((parts[2], parts[3]), axis=1)
        return np.concatenate((top_half, bottom_half), axis=0)

    def apply_gaussian_kernel(img, kernel):
        h, w = img.shape
        padding = kernel.shape[0] // 2
        padded_img = np.pad(img, ((padding, padding), (padding, padding)), mode='constant', constant_values=0)
        output = np.zeros_like(img)
        
        for i in range(h):
            for j in range(w):
                region = padded_img[i:i+kernel.shape[0], j:j+kernel.shape[1]]
                output[i, j] = np.sum(region * kernel)
        
        return output

    parts = divide_and_conquer(image)
    blurred_parts = process_parts(parts)
    blurred_image = merge_parts(blurred_parts)
    return blurred_image

# Route utama untuk halaman upload
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk mengupload gambar dan memprosesnya
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    # Simpan gambar yang diupload
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    
    # Membaca gambar yang di-upload
    img = Image.open(filename).convert('L')
    img_array = np.array(img)

    # Terapkan Gaussian Blur
    blurred_image = gaussian_blur(img_array)

    # Simpan gambar hasil blur
    result_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'blurred_' + file.filename)
    blurred_img = Image.fromarray(blurred_image)
    blurred_img.save(result_filename)

    # Kembalikan gambar hasil kepada pengguna
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'blurred_' + file.filename)

if __name__ == '__main__':
    app.run(debug=True)
