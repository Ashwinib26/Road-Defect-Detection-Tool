from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', original_image=None, processed_image=None)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Process image
        result_path = process_image(filepath, filename)

        return render_template(
            'index.html',
            original_image=url_for('static', filename=f'uploads/{filename}'),
            processed_image=url_for('static', filename=f'results/{os.path.basename(result_path)}')
        )
    return redirect(url_for('index'))

def process_image(filepath, filename):
    # Load & Resize
    image = cv2.imread(filepath)
    resized = cv2.resize(image, (512, 512))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive Thresholding
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    # Edge detection (Canny)
    edges = cv2.Canny(blurred, 50, 150)

    # Morphology to close gaps and emphasize structures
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(edges, kernel, iterations=2)

    # Contour detection and filtering
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = resized.copy()
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 300:  # Filter noise
            cv2.drawContours(contour_image, [cnt], -1, (0, 255, 0), 2)

    # Save result
    result_path = os.path.join(RESULT_FOLDER, f'processed_{filename}')
    cv2.imwrite(result_path, contour_image)

    return result_path

if __name__ == '__main__':
    app.run(debug=True)
