from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from werkzeug.utils import secure_filename
from PIL import ImageOps
from PIL import Image  # Untuk fitur resize
from PIL import Image, ImageFilter
from compress import optimize_image  # Fungsi kompresi eksternal
from filters import blur_divide_and_conquer, grayscale_iterative, sharpen_divide_and_conquer, sepia_iterative, edge_detection_dp, selective_filter_backtracking

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/filtered'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Pastikan folder upload dan output ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Periksa apakah file memiliki ekstensi yang diizinkan."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Halaman utama."""
    return render_template('home.html')


# -------------------
# Fitur Kompresi Gambar
# -------------------
@app.route('/compress', methods=['GET', 'POST'])
def compress():
    """Tampilkan halaman upload dan opsi kompresi."""
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            return "No file uploaded or file name empty", 400
        if not allowed_file(file.filename):
            return "File type not allowed", 400

        filename = secure_filename(file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_path)

        original_size_kb = os.path.getsize(original_path) / 1024

        # Generate opsi kompresi
        compression_options = {f"{percent}%": round(original_size_kb * (percent / 100), 2)
                               for percent in [20, 30, 40, 50, 60, 70, 80, 90, 95]}

        fixed_options = {
            "100 KB": 0.1, "200 KB": 0.2, "300 KB": 0.3,
            "400 KB": 0.4, "500 KB": 0.5, "1 MB": 1, "2 MB": 2, "3 MB": 3
        }
        fixed_options = {label: size for label, size in fixed_options.items() if size * 1024 <= original_size_kb}

        return render_template('compress/choose_compress.html', filename=filename, file_size=round(original_size_kb, 2),
                               compression_options=compression_options, fixed_options=fixed_options, compressed=False)

    return render_template('compress/compress.html')


@app.route('/compress_image', methods=['POST'])
def compress_image():
    """Proses kompresi gambar."""
    filename = request.form.get('filename')
    target_size_mb = float(request.form.get('target_size_mb', 0))

    if not filename or not target_size_mb:
        return "Invalid input data", 400

    original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], f"compressed_{filename}")

    # Optimalkan gambar ke ukuran target
    target_size_kb = target_size_mb * 1024
    optimize_image(original_path, compressed_path, target_size_kb)

    compressed_size_kb = os.path.getsize(compressed_path) / 1024

    return render_template('compress/choose_compress.html', filename=filename, file_size=round(target_size_kb, 2),
                           compressed=True, compressed_size=round(compressed_size_kb, 2),
                           download_filename=f"compressed_{filename}")


# -------------------
# Fitur Resize Gambar
# -------------------
@app.route('/resize', methods=['GET', 'POST'])
def resize():
    """Fitur resize gambar."""
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            return "No file uploaded or file name empty", 400
        if not allowed_file(file.filename):
            return "File type not allowed", 400

        filename = secure_filename(file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_path)

        width = request.form.get('width', type=int)
        height = request.form.get('height', type=int)

        if not width or not height:
            return "Invalid width or height", 400

        resized_path = os.path.join(app.config['UPLOAD_FOLDER'], f"resized_{filename}")
        with Image.open(original_path) as img:
            img = img.resize((width, height))
            img.save(resized_path)

        resized_size_kb = os.path.getsize(resized_path) / 1024

        return render_template('resize/resize.html', filename=filename, width=width, height=height,
                       resized=True, resized_size=round(resized_size_kb, 2),
                       resized_image=f"resized_{filename}")

    return render_template('resize/resize.html', resized=False)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and redirect to filters page."""
    file = request.files.get('file')

    # Validasi file
    if not file or file.filename == '':
        return "No file uploaded or file name empty", 400
    if not allowed_file(file.filename):
        return "File type not allowed", 400

    # Simpan file secara aman
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Pindah ke halaman filters dan kirimkan nama file yang diupload
    return render_template('filter/filters.html', original=filename, filtered=None)


# -------------------
# Fitur Download File
# -------------------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Endpoint untuk mengunduh file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/filters', methods=['GET', 'POST'])
def apply_filter():
    """Halaman untuk fitur filter gambar."""
    if request.method == 'POST':
        file = request.files.get('file')
        selected_filter = request.form.get('filter')

        # Debugging: Cek apakah file dan filter tersedia
        if not file:
            print("DEBUG: No file uploaded")
            return "No file uploaded or file name empty", 400
        if not allowed_file(file.filename):
            print("DEBUG: File type not allowed")
            return "File type not allowed", 400
        if not selected_filter:
            print("DEBUG: No filter selected")
            return "No filter selected", 400

        # Simpan file yang diunggah
        filename = secure_filename(file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_path)
        print(f"DEBUG: File uploaded and saved at {original_path}")

        # Terapkan filter
        try:
            with Image.open(original_path) as img:
                img = img.convert('RGB')  # Konversi ke RGB untuk kompatibilitas
                print(f"DEBUG: Opened image: {original_path}")

                if selected_filter == 'blur':
                    print("DEBUG: Applying blur filter")
                    img = blur_divide_and_conquer(img)
                elif selected_filter == 'grayscale':
                    print("DEBUG: Applying grayscale filter")
                    img = grayscale_iterative(img)
                elif selected_filter == 'sharpen':
                    print("DEBUG: Applying sharpen filter")
                    img = sharpen_divide_and_conquer(img)
                elif selected_filter == 'sepia':
                    print("DEBUG: Applying sepia filter")
                    img = sepia_iterative(img)
                elif selected_filter == 'edge_detection':
                    print("DEBUG: Applying edge detection filter")
                    img = edge_detection_dp(img)
                elif selected_filter == 'selective_filter':
                    print("DEBUG: Applying selective filter")
                    target_color = (0, 0, 255)  # Contoh warna biru
                    replacement_color = (255, 0, 0)  # Contoh warna merah
                    img = selective_filter_backtracking(img, target_color, replacement_color)
                else:
                    print(f"DEBUG: Unknown filter selected: {selected_filter}")
                    return "Invalid filter selected", 400

                # Simpan gambar hasil filter
                filtered_filename = f"filtered_{filename}"
                filtered_path = os.path.join(app.config['OUTPUT_FOLDER'], filtered_filename)
                img.save(filtered_path)
                print(f"DEBUG: Filtered image saved at {filtered_path}")

        except Exception as e:
            print(f"DEBUG: Error applying filter: {str(e)}")
            return f"Error applying filter: {str(e)}", 500

        return render_template(
            'filter/filters.html',
            original=filename,
            filtered=filtered_filename,
        )

    return render_template('filter/filters.html', original=None, filtered=None)

if __name__ == '__main__':
    app.run(debug=True)
