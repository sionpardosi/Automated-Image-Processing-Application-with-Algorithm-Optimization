from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def optimize_image_to_target_size(input_path, output_path, target_size_mb):
    """
    Optimize an image to reach a target file size by adjusting quality and resolution.
    
    Parameters:
    - input_path: Path to the input image
    - output_path: Path to save the optimized image
    - target_size_mb: Target file size in MB
    """
    # Convert target size from MB to KB (1 MB = 1024 KB)
    target_size_kb = target_size_mb * 1024

    # Get the size of the original image (in KB)
    original_size_kb = os.path.getsize(input_path) / 1024  # Convert bytes to KB
    print(f"Original file size: {original_size_kb:.2f} KB")

    # Check if target size is greater than the original size
    if target_size_kb > original_size_kb:
        return f"Target size {target_size_mb} MB cannot be greater than the original file size of {original_size_kb:.2f} KB", 400

    with Image.open(input_path) as img:
        # Convert RGBA images to RGB to handle JPEG format compatibility
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Start by checking the resolution of the image
        img_width, img_height = img.size
        target_width = int(img_width * 0.8)  # Reducing width by 20%
        target_height = int(img_height * 0.8)  # Reducing height by 20%
        
        # If the image width is larger than the threshold, resize it
        if img_width > 1024:
            img = img.resize((target_width, target_height), Image.LANCZOS)

        # Start with high quality
        quality = 95
        img.save(output_path, format="JPEG", quality=quality, optimize=True)

        # Reduce quality iteratively until the file size is close to target_size_kb but not larger than original size
        while os.path.getsize(output_path) > target_size_kb * 1024 and quality > 10:
            quality -= 5  # Decrease quality in steps
            img.save(output_path, format="JPEG", quality=quality, optimize=True)

        # Ensure file size does not exceed original size
        if os.path.getsize(output_path) > original_size_kb * 1024:
            os.remove(output_path)  # Remove the file if it exceeds original size
            return f"Could not compress image to the desired size without exceeding original file size ({original_size_kb:.2f} KB).", 400

    return None

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

    # Save the original uploaded file
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(original_path)

    # Retrieve user-specified target size (in MB) and validate input
    target_size_mb = float(request.form.get('target_size_mb', 1))  # Default to 1 MB if not specified

    # Call the function to optimize image and check for error
    optimized_path = os.path.join(app.config['UPLOAD_FOLDER'], 'optimized_' + file.filename)
    error_message = optimize_image_to_target_size(original_path, optimized_path, target_size_mb)

    if error_message:
        return error_message

    # Return the optimized image for download
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'optimized_' + file.filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
