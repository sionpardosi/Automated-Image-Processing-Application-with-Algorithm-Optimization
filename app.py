from flask import Flask, render_template, request, url_for
from PIL import Image, ImageFilter
import os
import uuid
import numpy as np

app = Flask(__name__)

# Folder untuk mengunggah dan menyimpan hasil gambar
upload_folder = 'static/uploads'
os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Divide and Conquer - Thresholding
def threshold_image_divide_and_conquer(image):
    grayscale_image = image.convert('L')
    np_image = np.array(grayscale_image)
    threshold_value = 128
    binary_image = np.where(np_image > threshold_value, 255, 0).astype(np.uint8)
    return Image.fromarray(binary_image).convert('RGB')

# Divide and Conquer - Blur per Blok
def blur_image_divide_and_conquer(image, blur_radius):
    width, height = image.size
    blurred_image = image.copy()
    block_size = 100
    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            box = (x, y, min(x + block_size, width), min(y + block_size, height))
            region = image.crop(box)
            blurred_block = region.filter(ImageFilter.GaussianBlur(blur_radius))
            blurred_image.paste(blurred_block, box)
    return blurred_image

# Fungsi untuk mengonversi gambar menjadi hitam putih
def convert_to_black_and_white(image):
    return image.convert('L').convert('RGB')

# Fungsi untuk menyimpan gambar dan menghasilkan nama unik
def save_and_get_unique_filename(file):
    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    return unique_filename, file_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return "No file found", 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        unique_filename, file_path = save_and_get_unique_filename(file)
        original_image = Image.open(file_path)

        # Proses gambar berdasarkan pilihan
        action = request.form.get('action')
        result_images = {}

        if action == 'threshold':
            thresholded_image = threshold_image_divide_and_conquer(original_image)
            threshold_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'threshold_' + unique_filename)
            thresholded_image.save(threshold_filename)
            result_images['threshold'] = url_for('static', filename='uploads/threshold_' + unique_filename)

        elif action == 'blur':
            blur_radius = int(request.form.get('blur_radius', 5))
            blurred_image = blur_image_divide_and_conquer(original_image, blur_radius)
            blurred_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'blurred_' + unique_filename)
            blurred_image.save(blurred_filename)
            result_images['blurred'] = url_for('static', filename='uploads/blurred_' + unique_filename)

        elif action == 'black_white':
            black_and_white_image = convert_to_black_and_white(original_image)
            bw_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'bw_' + unique_filename)
            black_and_white_image.save(bw_filename)
            result_images['black_white'] = url_for('static', filename='uploads/bw_' + unique_filename)

        return render_template('result.html', 
                               original_image=url_for('static', filename='uploads/' + unique_filename),
                               result_images=result_images)
    return "Invalid file type", 400

if __name__ == '__main__':
    app.run(debug=True)
