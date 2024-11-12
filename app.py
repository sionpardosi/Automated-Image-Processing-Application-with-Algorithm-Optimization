from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def optimize_image(input_path, output_path, target_size_kb):
    """
    Optimize an image to achieve a target size using a greedy approach.
    
    Parameters:
    - input_path: Path to the input image
    - output_path: Path to save the optimized image
    - target_size_kb: Target file size in KB
    """
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Start with high quality and reduce quality in greedy steps
        quality = 95
        img.save(output_path, format="JPEG", quality=quality, optimize=True)

        # Greedy approach: reduce quality in increments of 5 until target size is reached or quality is too low
        while os.path.getsize(output_path) > target_size_kb * 1024 and quality > 10:
            # Greedy step: lower the quality by 5 and check file size
            quality -= 5
            img.save(output_path, format="JPEG", quality=quality, optimize=True)

            # Log the current file size to understand the effect of each greedy step
            current_size_kb = os.path.getsize(output_path) / 1024
            print(f"Quality: {quality} | Current file size: {current_size_kb:.2f} KB")

        # Check if the current file size is close to the target size
        if abs(os.path.getsize(output_path) / 1024 - target_size_kb) <= 5:
            print("Optimized size is within 5 KB of the target.")

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

    # Calculate the compression options dynamically based on original size
    compression_options = {}
    for percent in [20, 30, 40, 50, 60, 70, 80, 90, 95]:
        target_size_kb = original_size_kb * (percent / 100)
        compression_options[f"{percent}%"] = round(target_size_kb / 1024, 2)  # Convert to MB for display

    # Add fixed options if they are smaller than or equal to the original size
    fixed_options = {}
    possible_fixed_options = {
        "100 KB": 0.1,
        "200 KB": 0.2,
        "300 KB": 0.3,
        "400 KB": 0.4,
        "500 KB": 0.5,
        "600 KB": 0.6,
        "700 KB": 0.7,
        "800 KB": 0.8,
        "900 KB": 0.9,
        "1 MB": 1,
        "2 MB": 2,
        "3 MB": 3,
        "4 MB": 4,
        "5 MB": 5,
        "6 MB": 6,
        "7 MB": 7,
        "8 MB": 8,
        "9 MB": 9,
        "10 MB": 10,
        "12 MB": 12,
        "15 MB": 15,
        "20 MB": 20
    }

    for label, size_mb in possible_fixed_options.items():
        if size_mb * 1024 <= original_size_kb:  # Only include options <= original size
            fixed_options[label] = size_mb

    # Render the template with calculated options
    return render_template('choose_compression.html', 
                           file_size=original_size_kb, 
                           compression_options=compression_options, 
                           fixed_options=fixed_options,
                           filename=file.filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/compress', methods=['POST'])
def compress_image():
    # Get the target size selected by the user (in MB)
    target_size_mb = float(request.form['target_size_mb'])
    target_size_kb = int(target_size_mb * 1024)  # Convert MB to KB
    filename = request.form['filename']

    original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    optimized_path = os.path.join(app.config['UPLOAD_FOLDER'], 'optimized_' + filename)

    # Perform the compression based on the selected target size
    output_path = optimize_image(original_path, optimized_path, target_size_kb)

    # Return the optimized file to the user
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'optimized_' + filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
