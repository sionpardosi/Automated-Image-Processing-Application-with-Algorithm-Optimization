from flask import Flask, render_template, request, send_file, redirect, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)

# Konfigurasi folder upload dan resized
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESIZED_FOLDER'] = 'static/resized'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Pastikan folder upload ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Fungsi untuk memeriksa ekstensi file gambar
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Fungsi Greedy untuk kompresi gambar
def optimize_image(input_path, output_path, target_size_kb):
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Mulai dengan kualitas tinggi dan kurangi kualitas secara bertahap
        quality = 95
        img.save(output_path, format="JPEG", quality=quality, optimize=True)

        while os.path.getsize(output_path) > target_size_kb * 1024 and quality > 10:
            quality -= 5
            img.save(output_path, format="JPEG", quality=quality, optimize=True)

        if abs(os.path.getsize(output_path) / 1024 - target_size_kb) <= 5:
            print("Optimized size is within 5 KB of the target.")

    return output_path

# Fungsi Divide and Conquer untuk resize gambar
def divide_and_conquer_resize(img, new_width, new_height):
    original_width, original_height = img.size
    sections = []
    num_sections = 4  # Tentukan jumlah bagian yang diinginkan (misalnya 4 bagian)
    
    part_width = original_width // 2
    part_height = original_height // 2

    # Pisahkan gambar menjadi 4 bagian
    for i in range(2):
        for j in range(2):
            left = i * part_width
            upper = j * part_height
            right = (i + 1) * part_width
            lower = (j + 1) * part_height
            section = img.crop((left, upper, right, lower))
            sections.append(section)
    
    # Resize masing-masing bagian sesuai ukuran baru
    resized_sections = []
    for section in sections:
        resized_section = section.resize((new_width // 2, new_height // 2))
        resized_sections.append(resized_section)
    
    # Gabungkan kembali bagian-bagian gambar menjadi gambar yang utuh
    new_img = Image.new('RGB', (new_width, new_height))
    new_img.paste(resized_sections[0], (0, 0))
    new_img.paste(resized_sections[1], (new_width // 2, 0))
    new_img.paste(resized_sections[2], (0, new_height // 2))
    new_img.paste(resized_sections[3], (new_width // 2, new_height // 2))
    
    return new_img

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            img = Image.open(file_path)
            original_width, original_height = img.size

            # Cek apakah ingin resize atau kompresi
            if 'resize' in request.form:
                new_width = request.form.get('new_width')
                new_height = request.form.get('new_height')

                if new_width and new_height:
                    new_width = int(new_width)
                    new_height = int(new_height)
                    resized_img = divide_and_conquer_resize(img, new_width, new_height)
                    resized_filename = f"resized_{filename}"
                    resized_file_path = os.path.join(app.config['RESIZED_FOLDER'], resized_filename)

                    if not os.path.exists(app.config['RESIZED_FOLDER']):
                        os.makedirs(app.config['RESIZED_FOLDER'])

                    resized_img.save(resized_file_path)

                    return render_template('index.html', uploaded_image=filename, resized_image=resized_filename,
                                           original_width=original_width, original_height=original_height,
                                           new_width=new_width, new_height=new_height)

            if 'compress' in request.form:
                target_size_mb = float(request.form['target_size_mb'])
                target_size_kb = int(target_size_mb * 1024)  # Convert MB to KB
                optimized_filename = f"optimized_{filename}"
                optimized_file_path = os.path.join(app.config['UPLOAD_FOLDER'], optimized_filename)
                
                optimized_path = optimize_image(file_path, optimized_file_path, target_size_kb)

                # Mendapatkan ukuran file yang telah dikompresi
                compressed_size_kb = os.path.getsize(optimized_path) / 1024
                compressed_size_mb = compressed_size_kb / 1024

                return render_template('download.html', compressed_file=optimized_filename,
                                       compressed_size_kb=compressed_size_kb, compressed_size_mb=compressed_size_mb)

    return render_template('index.html')


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['RESIZED_FOLDER'], filename), as_attachment=True)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
