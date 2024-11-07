from flask import Flask, request, render_template, url_for
from PIL import Image
import os
import json

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def create_upload_folder():
    """Create the upload folder if it doesn't exist"""
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def save_and_get_unique_filename(file):
    """Save file and return its unique filename"""
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    print(f"Saved file to: {file_path}")  # Debug print
    return filename, file_path

def process_crop_image(file_path, crop_data):
    """Crop the image to desired dimensions"""
    original_image = Image.open(file_path)
    cropped_image = original_image.crop((
        crop_data['left'],
        crop_data['top'],
        crop_data['left'] + crop_data['width'],
        crop_data['top'] + crop_data['height']
    ))
    return cropped_image

def process_resize_image(image, resize_width, resize_height):
    """Resize the image to desired dimensions"""
    resized_image = image.resize((resize_width, resize_height))
    return resized_image

@app.route('/')
def index():
    """Render the index (homepage)"""
    return render_template('index.html')

@app.route('/crop_and_resize', methods=['POST'])
def crop_and_resize():
    """Handle crop and resize functionality"""
    create_upload_folder()

    if 'file' not in request.files:
        return render_template('index.html', result_image=None, message="No file uploaded.")

    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', result_image=None, message="No file selected.")

    if file:
        unique_filename, file_path = save_and_get_unique_filename(file)

        # Get the crop and resize data from the form
        crop_width = int(request.form['crop_width'])
        crop_height = int(request.form['crop_height'])
        resize_width = int(request.form['resize_width'])
        resize_height = int(request.form['resize_height'])

        # Get the crop data from the hidden field
        crop_data = json.loads(request.form['crop_data'])

        try:
            # Crop the image using the crop data
            cropped_image = process_crop_image(file_path, crop_data)
            cropped_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cropped_' + unique_filename)
            cropped_image.save(cropped_path)

            # Resize the cropped image
            resized_image = process_resize_image(cropped_image, resize_width, resize_height)
            resized_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resized_' + unique_filename)
            resized_image.save(resized_path)

            result_url = url_for('uploaded_file', filename='resized_' + unique_filename)
            return render_template('index.html', result_image=result_url, message="Image processed successfully.")
        
        except Exception as e:
            return render_template('index.html', result_image=None, message=f"Error: {str(e)}")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve the processed image"""
    return app.send_static_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == "__main__":
    app.run(debug=True)
