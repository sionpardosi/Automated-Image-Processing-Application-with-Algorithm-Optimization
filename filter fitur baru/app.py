from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageFilter
import os
import io

app = Flask(__name__)

# Direktori untuk menyimpan gambar yang diunggah dan hasil filter
UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'static/output/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Membuat direktori jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Filter Functions (mempertahankan fungsi filter seperti sebelumnya)
def blur_divide_and_conquer(img):
    width, height = img.size
    quadrants = [
        img.crop((0, 0, width // 2, height // 2)),
        img.crop((width // 2, 0, width, height // 2)),
        img.crop((0, height // 2, width // 2, height)),
        img.crop((width // 2, height // 2, width, height))
    ]
    
    blurred_quadrants = [q.filter(ImageFilter.GaussianBlur(radius=5)) for q in quadrants]
    
    img.paste(blurred_quadrants[0], (0, 0))
    img.paste(blurred_quadrants[1], (width // 2, 0))
    img.paste(blurred_quadrants[2], (0, height // 2))
    img.paste(blurred_quadrants[3], (width // 2, height // 2))
    
    return img

def grayscale_iterative(img):
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            gray_value = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
            img.putpixel((x, y), (gray_value, gray_value, gray_value))
    return img

def sharpen_divide_and_conquer(img):
    width, height = img.size
    quadrants = [
        img.crop((0, 0, width // 2, height // 2)),
        img.crop((width // 2, 0, width, height // 2)),
        img.crop((0, height // 2, width // 2, height)),
        img.crop((width // 2, height // 2, width, height))
    ]
    sharpened_quadrants = [q.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)) for q in quadrants]
    img.paste(sharpened_quadrants[0], (0, 0))
    img.paste(sharpened_quadrants[1], (width // 2, 0))
    img.paste(sharpened_quadrants[2], (0, height // 2))
    img.paste(sharpened_quadrants[3], (width // 2, height // 2))
    return img

def sepia_iterative(img):
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            red, green, blue = pixel[0], pixel[1], pixel[2]
            tr = int(0.393 * red + 0.769 * green + 0.189 * blue)
            tg = int(0.349 * red + 0.686 * green + 0.168 * blue)
            tb = int(0.272 * red + 0.534 * green + 0.131 * blue)
            img.putpixel((x, y), (min(255, tr), min(255, tg), min(255, tb)))
    return img

def edge_detection_dp(img):
    width, height = img.size
    gray = grayscale_iterative(img)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    return edges

def selective_filter_backtracking(img, target_color, replacement_color, tolerance=30):
    width, height = img.size
    pixels = img.load()

    def is_similar(color1, color2):
        return all(abs(color1[i] - color2[i]) <= tolerance for i in range(3))

    def backtrack(x, y, visited):
        if (x, y) in visited or x < 0 or x >= width or y < 0 or y >= height:
            return
        if not is_similar(pixels[x, y], target_color):
            return

        visited.add((x, y))
        pixels[x, y] = replacement_color
        backtrack(x + 1, y, visited)
        backtrack(x - 1, y, visited)
        backtrack(x, y + 1, visited)
        backtrack(x, y - 1, visited)

    visited = set()
    for x in range(width):
        for y in range(height):
            if is_similar(pixels[x, y], target_color) and (x, y) not in visited:
                backtrack(x, y, visited)
    return img

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file:
        img = Image.open(file)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        img.save(file_path)
        return redirect(url_for('filters', filename=file.filename))
    
    return redirect(url_for('index'))

@app.route('/filters/<filename>', methods=['GET', 'POST'])
def filters(filename):
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    img = Image.open(img_path)
    
    if request.method == 'POST':
        filter_type = request.form['filter']
        
        if filter_type == 'blur':
            img = blur_divide_and_conquer(img)
        elif filter_type == 'grayscale':
            img = grayscale_iterative(img)
        elif filter_type == 'sharpen':
            img = sharpen_divide_and_conquer(img)
        elif filter_type == 'sepia':
            img = sepia_iterative(img)
        elif filter_type == 'edge_detection':
            img = edge_detection_dp(img)
        elif filter_type == 'selective_filter':
            target_color = (255, 0, 0)  # Red
            replacement_color = (0, 255, 0)  # Green
            img = selective_filter_backtracking(img, target_color, replacement_color)

        # Save the filtered image with a unique name
        output_filename = f"filtered_{filter_type}_{filename}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        img.save(output_path)

        # Return the template with both original and filtered images
        return render_template('filters.html', original=filename, filtered=output_filename)

    # For the initial load, just display the original image
    return render_template('filters.html', original=filename)


if __name__ == '__main__':
    app.run(debug=True)
