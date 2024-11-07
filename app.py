from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def optimize_image(input_path, output_path, compression_ratio):
    """
    Optimize an image based on the compression ratio selected by the user.
    
    Parameters:
    - input_path: Path to the input image
    - output_path: Path to save the optimized image
    - compression_ratio: Ratio to compress the image (e.g., 0.5 for 50%)
    """
    original_size_kb = os.path.getsize(input_path) / 1024  # Convert bytes to KB
    print(f"Original file size: {original_size_kb:.2f} KB")

    # Calculate target size based on compression ratio
    target_size_kb = original_size_kb * compression_ratio
    target_size_kb = int(target_size_kb)  # Convert to integer KB for calculation

    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        quality = 95
        img.save(output_path, format="JPEG", quality=quality, optimize=True)

        # Decrease quality until target size is reached or quality is too low
        while os.path.getsize(output_path) > target_size_kb * 1024 and quality > 10:
            quality -= 5
            img.save(output_path, format="JPEG", quality=quality, optimize=True)

    return output_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    original_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(original_path)

    # Calculate the file size in KB
    original_size_kb = os.path.getsize(original_path) / 1024  # KB
    print(f"File size before compression: {original_size_kb:.2f} KB")

    # Provide compression ratio options for the user
    compression_options = {
        '50%': 0.5,
        '75%': 0.75,
        '90%': 0.9
    }

    # Render the template with file size and compression options
    return render_template('choose_compression.html', 
                           file_size=original_size_kb, 
                           compression_options=compression_options, 
                           filename=file.filename)

@app.route('/compress', methods=['POST'])
def compress_image():
    # Get the compression ratio selected by the user
    compression_ratio = float(request.form['compression_ratio'])
    filename = request.form['filename']

    original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    optimized_path = os.path.join(app.config['UPLOAD_FOLDER'], 'optimized_' + filename)

    # Perform the compression based on the selected ratio
    output_path = optimize_image(original_path, optimized_path, compression_ratio)

    # Return the optimized file to the user
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'optimized_' + filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
