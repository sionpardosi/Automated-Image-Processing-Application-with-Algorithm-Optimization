from flask import Flask, render_template, request, redirect, url_for
from index import process_image
import os

app = Flask(__name__)

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk memproses gambar
@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    
    # Mengambil file gambar dan efek yang dipilih dari formulir
    image = request.files['image']
    effect = request.form['effect']
    
    # Memproses gambar dengan efek yang dipilih
    result_path = process_image(image, effect)
    
    # Periksa apakah gambar hasil telah berhasil disimpan
    if not os.path.exists(result_path):
        return render_template('index.html', error="Gagal memproses gambar.")
    
    # Menampilkan hasil gambar pada halaman yang sama
    return render_template('index.html', result_image=url_for('static', filename='processed_image.jpg'))

# Memulai server Flask
if __name__ == '__main__':
    app.run(debug=True)
